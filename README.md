# Video Compressor

This script compresses a video to an approximate target size using FFmpeg's
two-pass H.264 encoding. The output is an MP4 file with AAC audio and
fast-start metadata, which is suitable for uploading or streaming.

## Requirements

- Windows
- Python 3.8 or newer
- FFmpeg, including `ffmpeg.exe` and `ffprobe.exe`
- FFmpeg must be available in the system `PATH`

Verify that FFmpeg is installed and available by opening PowerShell and
running:

```powershell
ffmpeg -version
ffprobe -version
python --version
```

If either FFmpeg command is not recognized, install FFmpeg and add its `bin`
folder to the Windows `PATH`. Restart PowerShell after changing `PATH`.

## Installing FFmpeg

### Windows

Using [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/):

```powershell
winget install Gyan.FFmpeg.Shared
```

Alternatively, if you use [Chocolatey](https://chocolatey.org/):

```powershell
choco install ffmpeg
```

Close and reopen PowerShell after installation, then verify:

```powershell
ffmpeg -version
ffprobe -version
```

### macOS

Install [Homebrew](https://brew.sh/) if it is not already installed, then run:

```bash
brew install ffmpeg
```

Verify the installation:

```bash
ffmpeg -version
ffprobe -version
```

### Linux

For Ubuntu or Debian:

```bash
sudo apt update
sudo apt install ffmpeg
```

For Fedora:

```bash
sudo dnf install ffmpeg
```

For Arch Linux:

```bash
sudo pacman -S ffmpeg
```

Verify the installation:

```bash
ffmpeg -version
ffprobe -version
```

## Setup

1. Open [video_compressor.py](video_compressor.py) in a text editor.
2. Set `INPUT_VIDEO_PATH` to the full path of the video to compress.
3. Set `TARGET_SIZE_MB` to the desired approximate output size.

Example:

```python
INPUT_VIDEO_PATH = r"C:\Users\YourName\Videos\input.mp4"
TARGET_SIZE_MB = 150
```

The target size must be between **100 MB and 200 MB**, inclusive. The script
uses a raw string (`r"..."`) so Windows backslashes do not need to be escaped.

## Run the script

Open PowerShell in this project folder and run:

```powershell
python .\video_compressor.py
```

The script performs two FFmpeg passes:

1. An analysis pass to calculate the required video bitrate.
2. An encoding pass that creates the compressed video.

The result is saved as:

```text
C:\Users\<your-user-name>\Downloads\compressed_vid.mp4
```

The script prints the FFmpeg commands it runs and the approximate size of the
created file.

## Important behavior

- The original video is not modified.
- The output file is overwritten if `compressed_vid.mp4` already exists.
- Audio is encoded as AAC at 128 kbps.
- Video is encoded as H.264 (`libx264`) using the `medium` preset.
- The requested size is approximate; duration, audio, and MP4 container
  overhead affect the final size.
- Very long videos may fail because the calculated video bitrate would be too
  low. In that case, choose a larger target size or use a shorter video.

## Troubleshooting

### `FFmpeg and FFprobe must be installed and available in PATH`

Install FFmpeg and ensure both `ffmpeg` and `ffprobe` can be run directly from
PowerShell. Restart the terminal after updating `PATH`.

### `Input video was not found`

Check that `INPUT_VIDEO_PATH` is a complete, correct path and that the file
exists. Keep the path in a raw Python string, for example:

```python
INPUT_VIDEO_PATH = r"C:\Users\YourName\Videos\input.mp4"
```

### `target_mb must be between 100 and 200`

Change `TARGET_SIZE_MB` to a value from 100 through 200.

### `The video is too long for the selected target size`

Use a larger target size, if appropriate, or shorten the input video before
running the script again.

### Python or FFmpeg command is not recognized

Install Python or FFmpeg, then ensure the relevant executable folder is added
to the Windows `PATH`. Open a new PowerShell window and retry the verification
commands in the Requirements section.

## Project files

```text
video_compressor.py   Compression script
README.md             Usage instructions
```
