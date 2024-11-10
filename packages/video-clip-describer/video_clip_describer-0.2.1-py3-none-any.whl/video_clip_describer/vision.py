from __future__ import annotations

import base64
from dataclasses import dataclass, field
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
import tempfile
from typing import TYPE_CHECKING

import cv2
import imagehash
import numpy as np
from openai import AsyncClient
from PIL import Image

from .const import (
    DESCRIPTION_REFORMAT_PROMPT,
    LOGGER as _LOGGER,
    VISION_PROMPT,
    VISION_PROMPT_GRID,
)

if TYPE_CHECKING:
    from os import PathLike


@dataclass
class VisionAgent:
    video_file: PathLike | None = None
    """Video file to describe."""
    api_base_url: str | None = "https://api.openai.com/v1"
    """API base URL to use for the LLM."""
    api_key: str | None = None
    """API key to use for the LLM."""
    vision_model: str = "gemini-1.5-pro"
    """LLM model to use for vision."""
    refine_model: str = "claude-3-5-sonnet"
    """LLM model to use for refinement of the description."""
    vision_prompt: str | None = None
    """Prompt to send to the LLM to describe the video."""
    refine_prompt: str | None = None
    """Prompt to send to the LLM to reformat the description."""
    prompt_context: str | None = None
    """Context to add to the prompt (will be replaced with {context} in the prompt)."""
    resize_video: tuple[int, int] = (640, 360)
    """Resize the video before sending to the LLM."""
    stack_grid: bool = False
    """Put video frames in a grid before sending to the LLM."""
    stack_grid_size: tuple[int, int] = (3, 3)
    """Grid size to stack frames in."""
    remove_similar_frames: bool = True
    """Remove similar frames before sending to the LLM."""
    hashing_max_frames: int = 200
    """Maximum number of frames to hash."""
    hash_size: int = 12
    """Hash size to use when hashing frames. Lower value means more frames are removed."""
    debug: bool = False
    """Debug mode."""
    debug_dir: PathLike | str = "./debug"
    """Directory to save debug files to."""

    _debug_dir: Path = field(init=False)
    _prompt_vars: dict[str, str] = field(init=False)

    def __post_init__(self):
        if self.video_file:
            self.video_file = Path(self.video_file)
        self.debug_dir = Path(self.debug_dir)
        if self.debug:
            run_name = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%S")
            self._debug_dir = Path(self.debug_dir) / run_name
            self._debug_dir.mkdir(parents=True, exist_ok=True)
        if self.stack_grid and self.vision_prompt is None:
            self.vision_prompt = VISION_PROMPT_GRID
        if self.vision_prompt is None:
            self.vision_prompt = VISION_PROMPT
        if self.refine_prompt is None:
            self.refine_prompt = DESCRIPTION_REFORMAT_PROMPT

        self._prompt_vars = {}
        if self.prompt_context is not None:
            self._prompt_vars["context"] = self.prompt_context

        self.openai = AsyncClient(base_url=self.api_base_url, api_key=self.api_key)

    def _remove_similar_frames(
        self,
        base64_frames: list[str],
    ) -> list[str]:
        base64_hashing_frames = []
        hashes = []
        total_frames = len(base64_frames)
        hash_size = self.hash_size
        resize_ar = self.resize_video[0] / self.resize_video[1]
        resize_hashing = (256, round(256 / resize_ar))

        for idx in range(total_frames):
            frame = cv2.imdecode(
                np.frombuffer(base64.b64decode(base64_frames[idx]), np.uint8), cv2.IMREAD_COLOR
            )
            hashing_frame = cv2.resize(frame, resize_hashing)
            _, buffer = cv2.imencode(".jpg", hashing_frame)
            base64_hashing_frames.append(base64.b64encode(buffer).decode("utf-8"))

        while total_frames > self.hashing_max_frames:
            _LOGGER.info(
                "Hashing %d frames with hash size %d",
                len(base64_frames),
                hash_size,
            )
            hashes = []
            for frame in base64_hashing_frames:
                im = Image.open(BytesIO(base64.b64decode(frame)))
                frame_hash = imagehash.average_hash(im, hash_size)
                hashes.append(str(frame_hash))
            total_frames = len(list(dict.fromkeys(hashes)))
            hash_size -= 1
            _LOGGER.info("Result: %d frames", total_frames)

        if len(hashes) > 0:
            keep_frames = []
            keep_frames_hashes = []
            for x, frame_hash in enumerate(hashes):
                if frame_hash in keep_frames_hashes:
                    continue
                if x == 0 or frame_hash != hashes[x - 1]:
                    keep_frames.append(base64_frames[x])
                    keep_frames_hashes.append(frame_hash)

            _LOGGER.info("Got %d frames after removing similar frames", len(keep_frames))
            base64_frames = keep_frames

        return base64_frames

    def _make_grid(
        self,
        base64_frames: list[str],
        *,
        line_thickness=5,
        jpeg_quality=70,
    ):
        grid_x, grid_y = self.stack_grid_size
        grid_size = grid_x * grid_y
        grid_frames = []
        num_full_grids = len(base64_frames) // grid_size

        grid_width = self.resize_video[0] * grid_x + line_thickness * (grid_x - 1)
        grid_height = self.resize_video[1] * grid_y + line_thickness * (grid_y - 1)

        for i in range(num_full_grids):
            grid = np.full((grid_height, grid_width, 3), 255, dtype=np.uint8)
            for y in range(grid_y):
                for x in range(grid_x):
                    idx = i * grid_size + y * grid_x + x
                    frame = cv2.imdecode(
                        np.frombuffer(base64.b64decode(base64_frames[idx]), np.uint8), cv2.IMREAD_COLOR
                    )
                    top_left_y = y * (self.resize_video[1] + line_thickness)
                    top_left_x = x * (self.resize_video[0] + line_thickness)
                    grid[
                        top_left_y : top_left_y + self.resize_video[1],
                        top_left_x : top_left_x + self.resize_video[0],
                    ] = frame

            _, buffer = cv2.imencode(
                ".jpg",
                cv2.resize(grid, self.resize_video),
                [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality],
            )
            grid_frames.append(base64.b64encode(buffer).decode("utf-8"))
        return grid_frames

    async def video_to_frames(
        self,
        video_data: bytes | None = None,
    ):
        """Generate jpg-encoded frames from a video."""
        if video_data:
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
                temp_file.write(video_data)
                temp_path = temp_file.name
            video = cv2.VideoCapture(temp_path)
        else:
            video = cv2.VideoCapture(str(self.video_file))

        base64_frames = []
        while video.isOpened():
            success, frame = video.read()
            if not success:
                break
            frame = cv2.resize(frame, self.resize_video)
            _, buffer = cv2.imencode(".jpg", frame)
            base64_frames.append(base64.b64encode(buffer).decode("utf-8"))

        _LOGGER.info("Extracted %d frames from video", len(base64_frames))
        video.release()

        if self.remove_similar_frames:
            base64_frames = self._remove_similar_frames(base64_frames)

        if self.debug:
            for x, f in enumerate(base64_frames):
                im = cv2.imdecode(np.frombuffer(base64.b64decode(f), np.uint8), cv2.IMREAD_COLOR)
                frame_path = self._debug_dir / f"frame{x:03d}.jpg"
                cv2.imwrite(str(frame_path), im)

        if self.stack_grid:
            base64_frames = self._make_grid(base64_frames)
            _LOGGER.info("Created %d grid frames", len(base64_frames))

            if self.debug:
                for x, f in enumerate(base64_frames):
                    im = cv2.imdecode(np.frombuffer(base64.b64decode(f), np.uint8), cv2.IMREAD_COLOR)
                    frame_path = self._debug_dir / f"grid{x:03d}.jpg"
                    cv2.imwrite(str(frame_path), im)

        return base64_frames

    async def describe_frames(
        self,
        b64_frames: list[str],
        *,
        prompt: str | None = None,
        context: str | None = None,
        model: str | None = None,
    ):
        """Send a request to vision-enabled LLM to describe a series of frames."""
        if prompt is None:
            prompt = self.vision_prompt
        if model is None:
            model = self.vision_model

        prompt_vars = self._prompt_vars
        if context is not None:
            prompt_vars["context"] = context
        prompt = prompt.format(**prompt_vars)

        params = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        *[
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{x}",
                                },
                            }
                            for x in b64_frames
                        ],
                    ],
                },
            ],
            "max_tokens": 200,
            "temperature": 0,
        }
        result = await self.openai.chat.completions.create(**params)
        return result.choices[0].message.content

    async def run(
        self,
        video_data: bytes | None = None,
        video_file: PathLike | None = None,
        test=False,
    ):
        """Generate a description from video."""
        if video_file is not None:
            self.video_file = Path(video_file)

        frames = await self.video_to_frames(video_data)

        if not test:
            description = await self.describe_frames(frames)

            _LOGGER.info("Got description: %s", description)

            params = {
                "model": self.refine_model,
                "messages": [
                    {
                        "role": "system",
                        "content": DESCRIPTION_REFORMAT_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": description,
                    },
                ],
                "temperature": 0,
                "max_tokens": 250,
            }

            result = await self.openai.chat.completions.create(**params)
            return result.choices[0].message.content

        return "[Test only]"
