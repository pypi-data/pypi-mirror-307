# video-clip-describer

## Installation

```bash
pip install video-clip-describer
```

## Usage

```python
import asyncio
from video_clip_describer import VisionAgent

agent = VisionAgent(
    "~/Videos/test.mp4",
    api_base_url="https://my-litellm-proxy.local/v1",
    api_key="sk-apikey",
    vision_model="claude-3-5-sonnet",
    refine_model="gemini-1.5-flash",
    stack_grid=True,
    stack_grid_size=(3, 3),
    resize_video=(1024, 768),
    hashing_max_frames=200,
    hash_size=8,
    debug=True,
    debug_dir="./debug",
)

description = asyncio.run(agent.run())
print(description)
```

## CLI

```bash
$ video2text path/to/video.mp4
```

```bash
$ video2text --help

 Usage: video2text [OPTIONS] VIDEO_FILE

╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    video_file      FILENAME  The video file to process. [required]                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --resize                      <width>x<height>  Resize frames before sending to GPT-V. [default: 1024x768]                                       │
│ --stack-grid                                    Put video frames in a grid before sending to GPT-V.                                              │
│ --stack-grid-size             <cols>x<rows>     Grid size to stack frames in. [default: 3x3]                                                     │
│ --context                                       Context to add to prompt. [default: None]                                                        │
│ --api-base-url                                  OpenAI API compatible base URL. [env var: OPENAI_BASE_URL] [default: https://api.openai.com/v1]  │
│ --api-key                                       OpenAI API key. [env var: OPENAI_API_KEY]                                                        │
│ --model                                         LLM model to use (overrides --vision-model and --refine-model). [default: None]                  │
│ --vision-model                                  LLM model to use for vision. [default: claude-3-5-sonnet]                                        │
│ --refine-model                                  LLM model to use for refinement. [default: gemini-1.5-flash]                                     │
│ --no-compress                                   Don't remove similar frames before sending to GPT-V.                                             │
│ --max-frames                                    Max number of frames to allow before decreasing hashing length. [default: 200]                   │
│ --debug                                         Enable debugging.                                                                                │
│ --debug-dir                   PATH              Directory to output debug frames to if --debug is enabled. [default: ./debug]                    │
│                       -v                        Enable verbose output. Repeat for increased verbosity.                                           │
│ --test                                          Don't send requests to LLM.                                                                      │
│ --install-completion                            Install completion for the current shell.                                                        │
│ --show-completion                               Show completion for the current shell, to copy it or customize the installation.                 │
│ --help                                          Show this message and exit.                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```