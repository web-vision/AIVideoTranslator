import pysrt
from TTS.api import TTS

# === Konfiguration ===
SRT_FILE = "audio.wav.en.srt"
MODEL_NAME = "tts_models/en/vctk/vits"
# =====================

print("📖 Lade Untertitel...")
subs = pysrt.open(SRT_FILE)

print(f"🔊 Lade Coqui TTS Modell: {MODEL_NAME} (bitte kurz warten)...")
tts = TTS(model_name=MODEL_NAME, progress_bar=False, gpu=False)

# Liste der Sprecher:innen
speakers = tts.speakers
print("\n🎙️ Verfügbare Stimmen:")
for idx, speaker in enumerate(speakers):
    print(f"  [{idx+1}] {speaker}")

# Auswahl im Terminal
while True:
    try:
        selection = int(input("\n🗳️ Gib die Nummer der gewünschten Stimme ein: ")) - 1
        if 0 <= selection < len(speakers):
            selected_speaker = speakers[selection]
            print(f"✅ Stimme gewählt: {selected_speaker}")
            break
        else:
            print("❌ Nummer außerhalb des gültigen Bereichs.")
    except ValueError:
        print("❌ Bitte eine gültige Zahl eingeben.")

# Sprachclips generieren
print("\n🎧 Sprachsynthese beginnt...")
for i, sub in enumerate(subs):
    text = sub.text.replace('\n', ' ')
    output_file = f"clip_{i:03d}.wav"
    print(f"🔈 [{i+1}/{len(subs)}] → {output_file}")
    tts.tts_to_file(text=text, file_path=output_file, speaker=selected_speaker)

print("\n✅ Alle Clips erfolgreich generiert.")
