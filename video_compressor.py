import json
import shutil
import subprocess
import tempfile
from pathlib import Path


# Edit these two values before running the script.
INPUT_VIDEO_PATH = r"C:\Users\akars\Downloads\SPG Project Interview.mp4"
TARGET_SIZE_MB = 150


def run(command):
    print("Running:", " ".join(map(str, command)))
    subprocess.run(command, check=True)


def get_duration(input_file):
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "json",
            str(input_file),
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    return float(json.loads(result.stdout)["format"]["duration"])


def compress_video(input_file, output_file, target_mb=150):
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        raise RuntimeError("FFmpeg and FFprobe must be installed and available in PATH.")

    if not 100 <= target_mb <= 200:
        raise ValueError("target_mb must be between 100 and 200.")

    duration = get_duration(input_file)

    # Reserve space for audio and MP4 container overhead.
    audio_bitrate = 128_000
    target_bits = target_mb * 1024 * 1024 * 8
    video_bitrate = int((target_bits * 0.98 / duration) - audio_bitrate)

    if video_bitrate < 100_000:
        raise ValueError("The video is too long for the selected target size.")

    video_bitrate_k = video_bitrate // 1000

    with tempfile.TemporaryDirectory() as temp_dir:
        pass_log = Path(temp_dir) / "ffmpeg_pass"

        # First pass: analyze the video.
        run([
            "ffmpeg",
            "-y",
            "-i", str(input_file),
            "-c:v", "libx264",
            "-b:v", f"{video_bitrate_k}k",
            "-preset", "medium",
            "-pass", "1",
            "-passlogfile", str(pass_log),
            "-an",
            "-f", "null",
            "NUL",
        ])

        # Second pass: create the compressed video.
        run([
            "ffmpeg",
            "-y",
            "-i", str(input_file),
            "-c:v", "libx264",
            "-b:v", f"{video_bitrate_k}k",
            "-preset", "medium",
            "-pass", "2",
            "-passlogfile", str(pass_log),
            "-c:a", "aac",
            "-b:a", "128k",
            "-movflags", "+faststart",
            str(output_file),
        ])

    actual_size = Path(output_file).stat().st_size / (1024 * 1024)
    print(f"\nCreated: {output_file}")
    print(f"Approximate size: {actual_size:.1f} MB")


if __name__ == "__main__":
    input_file = Path(INPUT_VIDEO_PATH)
    if not input_file.is_file():
        raise FileNotFoundError(f"Input video was not found: {input_file}")

    output_file = Path.home() / "Downloads" / "compressed_vid.mp4"
    compress_video(input_file, output_file, TARGET_SIZE_MB)