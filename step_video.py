import subprocess
import os
import sys
import glob
from video_config import CONFIG

TEMP_DIR = CONFIG.get("temp_dir", "temp")
SUBTITLE_MODE = CONFIG.get("subtitle_mode", "soft")
OUTPUT_DIR = "output"
INPUT_DIR = "input"

base_name = sys.argv[1] if len(sys.argv) > 1 else "default"
input_video = os.path.join(INPUT_DIR, f"{base_name}.mp4")
output_video = os.path.join(OUTPUT_DIR, f"{base_name}_en.mp4")
output_audio = os.path.join(TEMP_DIR, f"{base_name}_en.wav")
srt_file = os.path.join(TEMP_DIR, f"{base_name}_en.srt")
concat_file = os.path.join(TEMP_DIR, f"{base_name}_concat.txt")

os.makedirs(OUTPUT_DIR, exist_ok=True)

clips = sorted(glob.glob(f"{TEMP_DIR}/{base_name}_clip_*.wav"))
if not clips:
    print("❌ Keine Sprachclips gefunden.")
    exit(1)

cwd = os.getcwd()
os.chdir(TEMP_DIR)

if not os.path.exists(os.path.basename(output_audio)):
    subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0",
                    "-i", os.path.basename(concat_file),
                    "-c", "copy", os.path.basename(output_audio), "-y"])

print("🎬 Erstelle Ausgabevideo...")

if os.path.exists(os.path.basename(srt_file)):
    if SUBTITLE_MODE == "hard":
        subprocess.run([
            "ffmpeg", "-i", os.path.join(cwd, input_video),
            "-i", os.path.basename(output_audio),
            "-vf", f"subtitles={os.path.basename(srt_file)}",
            "-map", "0:v", "-map", "1:a",
            "-c:v", "libx264", "-c:a", "aac",
            "-shortest", os.path.join(cwd, output_video), "-y"
        ])
    else:
        subprocess.run([
            "ffmpeg", "-i", os.path.join(cwd, input_video),
            "-i", os.path.basename(output_audio),
            "-i", os.path.basename(srt_file),
            "-map", "0:v", "-map", "1:a", "-map", "2",
            "-c:v", "copy", "-c:a", "aac", "-c:s", "mov_text",
            "-shortest", os.path.join(cwd, output_video), "-y"
        ])
else:
    subprocess.run([
        "ffmpeg", "-i", os.path.join(cwd, input_video),
        "-i", os.path.basename(output_audio),
        "-map", "0:v", "-map", "1:a",
        "-c:v", "copy", "-shortest", os.path.join(cwd, output_video), "-y"
    ])

os.chdir(cwd)
print(f"✅ Video gespeichert: {output_video}")
