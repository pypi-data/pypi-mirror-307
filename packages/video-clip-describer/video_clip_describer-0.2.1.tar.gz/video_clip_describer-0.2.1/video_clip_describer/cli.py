from __future__ import annotations

import asyncio
import logging
import os
from pathlib import Path

from rich import print
import typer

from video_clip_describer.vision import VisionAgent

app = typer.Typer()

_LOGGER = logging.getLogger(__name__)


def _get_default(key: str) -> str:
    value = getattr(VisionAgent, key)
    if isinstance(value, tuple):
        value = f"{value[0]}x{value[1]}"
    return value


def _parse_size(value: str) -> tuple[int, ...]:
    ints = value.split("x")
    if len(ints) != 2:  # noqa: PLR2004
        raise ValueError(f"Invalid size: {value}")
    if not all(x.isdigit() for x in ints):
        raise ValueError(f"Invalid size: {value}")
    return tuple(map(int, ints))


def _is_valid_writable_dir(parser, x):
    """Check if directory exists and is writable."""
    if not Path(x).is_dir():
        parser.error(f"{x} is not a valid directory.")
    if not os.access(x, os.W_OK | os.X_OK):
        parser.error(f"{x} is not writable.")
    return Path(x)


async def run(args):
    video_file = Path(args["video_file"].name).resolve()
    if not video_file.is_file():
        raise FileNotFoundError("File not found: ", video_file)

    agent = VisionAgent(
        video_file,
        remove_similar_frames=not args["no_compress"],
        hashing_max_frames=args["max_frames"],
        stack_grid=args["stack_grid"],
        stack_grid_size=args["stack_grid_size"],
        resize_video=args["resize"],
        vision_model=args["vision_model"],
        refine_model=args["refine_model"],
        prompt_context=args["context"],
        debug=args["debug"],
        debug_dir=args["debug_dir"],
        api_base_url=args["api_base_url"],
        api_key=args["api_key"],
    )

    desc = await agent.run(
        test=args["test"],
    )
    print(desc)


@app.command()
def main(
    video_file: typer.FileBinaryRead = typer.Argument(
        help="The video file to process.",
        show_default=False,
    ),
    resize: str | None = typer.Option(
        _get_default("resize_video"),
        "--resize",
        help="Resize frames before sending to GPT-V.",
        parser=_parse_size,
        metavar="<width>x<height>",
    ),
    stack_grid: bool = typer.Option(
        False,
        "--stack-grid",
        help="Put video frames in a grid before sending to GPT-V.",
        show_default=False,
        is_flag=True,
    ),
    stack_grid_size: str | None = typer.Option(
        _get_default("stack_grid_size"),
        help="Grid size to stack frames in.",
        parser=_parse_size,
        metavar="<cols>x<rows>",
    ),
    context: str | None = typer.Option(
        None,
        help="Context to add to prompt.",
        metavar="",
    ),
    api_base_url: str = typer.Option(
        VisionAgent.api_base_url,
        help="OpenAI API compatible base URL.",
        envvar="OPENAI_BASE_URL",
        metavar="",
    ),
    api_key: str = typer.Option(
        None,
        help="OpenAI API key.",
        envvar="OPENAI_API_KEY",
        metavar="",
        show_default=False,
    ),
    model: str | None = typer.Option(
        None,
        help="LLM model to use (overrides --vision-model and --refine-model).",
        metavar="",
    ),
    vision_model: str | None = typer.Option(
        VisionAgent.vision_model,
        help="LLM model to use for vision.",
        metavar="",
    ),
    refine_model: str | None = typer.Option(
        VisionAgent.refine_model,
        help="LLM model to use for refinement.",
        metavar="",
    ),
    no_compress: bool = typer.Option(
        False,
        "--no-compress",
        help="Don't remove similar frames before sending to GPT-V.",
        show_default=False,
        is_flag=True,
    ),
    max_frames: int | None = typer.Option(
        VisionAgent.hashing_max_frames,
        help="Max number of frames to allow before decreasing hashing length.",
        metavar="",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Enable debugging.",
        show_default=False,
        is_flag=True,
    ),
    debug_dir: Path | None = typer.Option(
        VisionAgent.debug_dir,
        help="Directory to output debug frames to if --debug is enabled.",
    ),
    verbose: int = typer.Option(
        0,
        "-v",
        help="Enable verbose output. Repeat for increased verbosity.",
        show_default=False,
        metavar="",
        count=True,
    ),
    test: bool = typer.Option(
        False,
        "--test",
        help="Don't send requests to LLM.",
        show_default=False,
        is_flag=True,
    ),
):
    if model is not None:
        if vision_model is None:
            vision_model = model
        if refine_model is None:
            refine_model = model

    logging_level = logging.ERROR
    if debug:
        logging_level = logging.DEBUG
    if verbose:
        logging_level = 50 - (verbose * 10)
        if logging_level <= 0:
            logging_level = logging.NOTSET
    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s [%(name)-15.15s] [%(levelname)-8.8s]  %(message)s",
        handlers=[logging.StreamHandler()],
    )
    args = {
        "video_file": video_file,
        "resize": resize,
        "stack_grid": stack_grid,
        "stack_grid_size": stack_grid_size,
        "context": context,
        "model": model,
        "vision_model": vision_model,
        "refine_model": refine_model,
        "no_compress": no_compress,
        "max_frames": max_frames,
        "debug": debug,
        "debug_dir": debug_dir,
        "verbose": verbose,
        "test": test,
        "api_base_url": api_base_url,
        "api_key": api_key,
    }
    _LOGGER.info("Running with args: %s", args)

    asyncio.run(run(args))
