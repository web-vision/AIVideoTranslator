import os
import glob
import pysrt
import subprocess
import sys
from TTS.api import TTS
from video_config import CONFIG

TEMP_DIR = CONFIG.get("temp_dir", "temp")
SPEAKER = CONFIG.get("default_speaker", "p230")
MODEL_NAME = "tts_models/en/vctk/vits"

base_name = sys.argv[1] if len(sys.argv) > 1 else "default"
srt_file = os.path.join(TEMP_DIR, f"{base_name}_en.srt")
os.makedirs(TEMP_DIR, exist_ok=True)

if not os.path.exists(srt_file):
    print(f"❌ SRT nicht gefunden: {srt_file}")
    exit(1)

subs = pysrt.open(srt_file)
tts_model = TTS(model_name=MODEL_NAME, progress_bar=False, gpu=False)

clip_files = []
for i, sub in enumerate(subs):
    text = sub.text.replace('\n', ' ')
    out_file = os.path.join(TEMP_DIR, f"{base_name}_clip_{i:03d}.wav")
    tts_model.tts_to_file(text=text, file_path=out_file, speaker=SPEAKER)
    clip_files.append(out_file)

concat_file = os.path.join(TEMP_DIR, f"{base_name}_concat.txt")
output_audio = os.path.join(TEMP_DIR, f"{base_name}_en.wav")

with open(concat_file, "w") as f:
    for clip in clip_files:
        f.write(f"file '{os.path.basename(clip)}'\n")

cwd = os.getcwd()
os.chdir(TEMP_DIR)
subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0",
                "-i", os.path.basename(concat_file),
                "-c", "copy", os.path.basename(output_audio), "-y"])
os.chdir(cwd)

print(f"✅ Audio-Mix gespeichert: {output_audio}")
