import os
import subprocess
import whisper
import sys
from video_config import CONFIG

TEMP_DIR = CONFIG.get("temp_dir", "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

base_name = sys.argv[1] if len(sys.argv) > 1 else "default"
input_video = f"input/{base_name}.mp4"
audio_file = os.path.join(TEMP_DIR, f"{base_name}.wav")
srt_file = os.path.join(TEMP_DIR, f"{base_name}_en.srt")

if not os.path.exists(audio_file):
    print("🎞️ Extrahiere Audio...")
    subprocess.run(["ffmpeg", "-i", input_video, "-q:a", "0", "-map", "a", audio_file, "-y"])

print("🧠 Lade Whisper...")
model = whisper.load_model("medium")
result = model.transcribe(audio_file, task="translate", language="German")

with open(srt_file, "w", encoding="utf-8") as f:
    for seg in result["segments"]:
        start = seg["start"]
        end = seg["end"]
        text = seg["text"].strip()
        f.write(f"{seg['id'] + 1}\n")
        f.write(f"{int(start // 3600):02}:{int(start % 3600 // 60):02}:{int(start % 60):02},{int((start*1000)%1000):03} --> ")
        f.write(f"{int(end // 3600):02}:{int(end % 3600 // 60):02}:{int(end % 60):02},{int((end*1000)%1000):03}\n")
        f.write(f"{text}\n\n")

print(f"✅ SRT-Datei erstellt: {srt_file}")
