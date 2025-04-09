import os
import subprocess
import time
import pysrt
from TTS.api import TTS

# === Konfiguration ===
VIDEO_FILE = "input.mp4"
AUDIO_FILE = "audio.wav"
SRT_FILE = "audio.wav.en.srt"
OUTPUT_AUDIO = "english_voice.wav"
FINAL_VIDEO = "output_translated.mp4"
VOICE_GENDER = "male"  # Nur als Marker – wird später noch angepasst
# ======================

# 1. Extrahiere Audio aus dem Video
print("🎞️ Extrahiere Audio aus Video...")
subprocess.run(["ffmpeg", "-i", VIDEO_FILE, "-q:a", "0", "-map", "a", AUDIO_FILE, "-y"])

# 2. Whisper: Transkription & Übersetzung
print("🧠 Starte Whisper-Übersetzung...")
import whisper
model = whisper.load_model("medium")
result = model.transcribe(AUDIO_FILE, task="translate", language="German")

# 3. Speichere Übersetzung als .srt-Datei
with open(SRT_FILE, "w", encoding="utf-8") as f:
    for segment in result["segments"]:
        start = segment["start"]
        end = segment["end"]
        text = segment["text"].strip()

        start_time = f"{int(start // 3600):02}:{int(start % 3600 // 60):02}:{int(start % 60):02},{int((start * 1000) % 1000):03}"
        end_time = f"{int(end // 3600):02}:{int(end % 3600 // 60):02}:{int(end % 60):02},{int((end * 1000) % 1000):03}"

        f.write(f"{segment['id'] + 1}\n{start_time} --> {end_time}\n{text}\n\n")

# 4. Editier-Pause
print("\n✏️ Du kannst jetzt die Datei 'audio.wav.en.srt' manuell bearbeiten.")
print("➡️ Öffne sie in VS Code, Sublime, Aegisub o.ä.")
input("✅ Drücke ENTER, wenn du mit dem Bearbeiten fertig bist...\n")

# 5. Lade SRT-Datei
subs = pysrt.open(SRT_FILE)

# 6. Initialisiere Coqui TTS
print(f"🔊 Verwende Coqui TTS (männlich)...")
tts_model = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

# 7. Generiere Sprachclips
clips = []
for i, sub in enumerate(subs):
    text = sub.text.replace('\n', ' ')
    clip_name = f"clip_{i:03d}.wav"
    print(f"🗣️  Generiere Sprachclip {clip_name}...")
    tts_model.tts_to_file(text=text, file_path=clip_name)
    clips.append(clip_name)

# 8. Erstelle Liste für ffmpeg
with open("concat.txt", "w") as f:
    for clip in clips:
        f.write(f"file '{clip}'\n")

# 9. Füge Clips zusammen
print("🎧 Füge Sprachclips zusammen...")
subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "concat.txt", "-c", "copy", OUTPUT_AUDIO, "-y"])

# 10. Setze Audio ins Video ein
print("🎬 Setze neue Tonspur ins Video ein...")
subprocess.run([
    "ffmpeg", "-i", VIDEO_FILE, "-i", OUTPUT_AUDIO,
    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-shortest", FINAL_VIDEO, "-y"
])

print("\n✅ Fertig! Dein übersetztes Video heißt:", FINAL_VIDEO)
