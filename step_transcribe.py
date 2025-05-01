import os
import subprocess
import whisper
import sys
from video_config import CONFIG

TEMP_DIR = CONFIG.get("temp_dir", "temp")
SUBTITLE_DIR = "subtitles"
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(SUBTITLE_DIR, exist_ok=True)

base_name = sys.argv[1] if len(sys.argv) > 1 else "default"
input_video = f"input/{base_name}.mp4"
audio_file = os.path.join(TEMP_DIR, f"{base_name}.wav")
srt_de = os.path.join(SUBTITLE_DIR, f"{base_name}_de.srt")   # ✅ direkt in subtitles
srt_en = os.path.join(TEMP_DIR, f"{base_name}_en.srt")       # ✅ bleibt in temp

if not os.path.exists(audio_file):
    print("🎞️ Extrahiere Audio...")
    subprocess.run(["ffmpeg", "-i", input_video, "-q:a", "0", "-map", "a", audio_file, "-y"])

print("🧠 Lade Whisper...")
model = whisper.load_model("medium")

# ➤ 1. Transkription auf Deutsch
print("📝 Erstelle deutsche SRT...")
result_de = model.transcribe(audio_file, task="transcribe", language="de")

with open(srt_de, "w", encoding="utf-8") as f:
    for seg in result_de["segments"]:
        f.write(f"{seg['id'] + 1}\n")
        f.write(f"{int(seg['start'] // 3600):02}:{int(seg['start'] % 3600 // 60):02}:{int(seg['start'] % 60):02},{int((seg['start']*1000)%1000):03} --> ")
        f.write(f"{int(seg['end'] // 3600):02}:{int(seg['end'] % 3600 // 60):02}:{int(seg['end'] % 60):02},{int((seg['end']*1000)%1000):03}\n")
        f.write(f"{seg['text'].strip()}\n\n")

# ➤ 2. Übersetzung ins Englische
print("🌐 Erstelle englische SRT...")
result_en = model.transcribe(audio_file, task="translate", language="de")

with open(srt_en, "w", encoding="utf-8") as f:
    for seg in result_en["segments"]:
        f.write(f"{seg['id'] + 1}\n")
        f.write(f"{int(seg['start'] // 3600):02}:{int(seg['start'] % 3600 // 60):02}:{int(seg['start'] % 60):02},{int((seg['start']*1000)%1000):03} --> ")
        f.write(f"{int(seg['end'] // 3600):02}:{int(seg['end'] % 3600 // 60):02}:{int(seg['end'] % 60):02},{int((seg['end']*1000)%1000):03}\n")
        f.write(f"{seg['text'].strip()}\n\n")

print(f"✅ SRT-Dateien gespeichert:")
print(f"  - Deutsch (Original):  {srt_de}")
print(f"  - Englisch (Übers.):   {srt_en}")
