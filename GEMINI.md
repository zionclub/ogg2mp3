# Project: ogg2mp3

## Project Overview
`ogg2mp3` is a command-line utility designed for the efficient conversion of OGG Vorbis audio files to the MP3 format. The project aims to provide a simple, recursive, and high-performance solution for media management and format compatibility.

### Core Technologies (Anticipated)
- **Primary Language:** Python 3.10+
- **Audio Processing:** [FFmpeg](https://ffmpeg.org/) (External dependency)
- **CLI Interface:** `argparse` or `click`
- **Concurrency:** `concurrent.futures` for parallel batch processing

## Building and Running
*Note: This project is currently in its initialization phase.*

### Prerequisites
- Python 3.10 or higher.
- FFmpeg must be installed on the host system and available in the system PATH.

### Initial Setup
1.  **Environment:** It is recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    ```
2.  **Dependencies:** Future dependencies should be listed in `requirements.txt`.
    ```bash
    # Proposed initial dependencies:
    # pip install pyinstaller
    ```

### Compilation (Windows)
To generate a standalone `.exe`:
```bash
python -m PyInstaller --noconfirm --onefile --windowed --name "Ogg2Mp3Converter" converter_gui.py
```
Outputs will be in the `dist/` directory.

### Execution (Proposed)
The tool is intended to be used as follows:
```bash
python -m ogg2mp3.converter --input /path/to/ogg/files --output /path/to/output
```

## Development Conventions
- **Code Quality:** Adhere to PEP 8 standards. Use `black` for formatting and `ruff` for linting.
- **Type Safety:** Use Type Hints throughout the codebase to ensure clarity and catch potential errors early.
- **Testing:** Utilize `pytest` for all testing. Focus on:
    - Verifying FFmpeg command generation.
    - Handling missing input files or invalid formats.
    - Ensuring recursive directory traversal works as expected.
- **AI-Assisted Workflow:**
    - Use this `GEMINI.md` file as the source of truth for project rules.
    - Always verify changes with tests before considering a task complete.
    - Maintain minimal and focused diffs.

## Current Status & Next Steps
This project has been initialized as an empty repository. The immediate next steps are:
1.  Create the project structure (e.g., `src/ogg2mp3/`, `tests/`).
2.  Implement a basic CLI wrapper.
3.  Implement the core conversion logic using `subprocess` to call `ffmpeg`.
4.  Add a `README.md` and `LICENSE` file.
