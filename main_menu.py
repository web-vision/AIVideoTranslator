import os
import subprocess
import glob
from video_config import CONFIG

def run(script, args=""):
    os.system(f"python3 {script} {args}")

def clean_temp():
    temp_dir = CONFIG.get("temp_dir", "temp")
    if not os.path.exists(temp_dir):
        print("📁 Temp-Ordner ist leer.")
        return
    for file in os.listdir(temp_dir):
        if file.endswith(".srt"):
            continue  # SRT behalten!
        path = os.path.join(temp_dir, file)
        if os.path.isfile(path):
            os.remove(path)
    print(f"🧹 Temp-Ordner '{temp_dir}' bereinigt (SRT-Dateien behalten).")

def archive_srt(base_name):
    temp_dir = CONFIG.get("temp_dir", "temp")
    srt_src = os.path.join(temp_dir, f"{base_name}_en.srt")
    srt_dest = os.path.join("subtitles", f"{base_name}_en.srt")

    if os.path.exists(srt_src):
        os.makedirs("subtitles", exist_ok=True)
        subprocess.run(["cp", srt_src, srt_dest])
        print(f"📁 SRT archiviert: subtitles/{base_name}_en.srt")

def process_bulk():
    input_dir = "input"
    output_dir = "output"
    temp_dir = CONFIG.get("temp_dir", "temp")

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)

    video_files = sorted(glob.glob(f"{input_dir}/*.mp4"))
    if not video_files:
        print("❌ Keine Videos in 'input/' gefunden.")
        return

    for video_path in video_files:
        filename = os.path.basename(video_path)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, f"{base_name}_en.mp4")

        print(f"\n🎬 Verarbeite: {filename}")

        subprocess.run(["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", f"{temp_dir}/{base_name}.wav", "-y"])
        run("step_transcribe.py", base_name)
        run("apply_glossary.py", base_name)
        archive_srt(base_name)
        run("step_tts.py", base_name)
        run("step_video.py", base_name)
        clean_temp()

    print("\n✅ Alle Videos wurden verarbeitet.")

def reencode_existing():
    temp_dir = CONFIG.get("temp_dir", "temp")
    srt_files = sorted(glob.glob(f"{temp_dir}/*_en.srt"))

    if not srt_files:
        print("❌ Keine vorhandenen SRT-Dateien gefunden.")
        return

    for srt_path in srt_files:
        base_name = os.path.basename(srt_path).replace("_en.srt", "")
        print(f"\n♻️ Neu-Kodierung: {base_name}")

        run("apply_glossary.py", base_name)
        run("step_tts.py", base_name)
        run("step_video.py", base_name)
        archive_srt(base_name)
        clean_temp()

    print("\n✅ Alle vorhandenen SRTs wurden neu verarbeitet.")

def rebuild_from_existing_srt():
    temp_dir = CONFIG.get("temp_dir", "temp")
    srt_files = sorted(glob.glob(f"{temp_dir}/*_en.srt"))

    if not srt_files:
        print("❌ Keine SRT-Dateien in /temp gefunden.")
        return

    for srt_path in srt_files:
        base_name = os.path.basename(srt_path).replace("_en.srt", "")
        print(f"\n🔄 Rekonstruiere Video für: {base_name}")

        run("apply_glossary.py", base_name)
        run("step_tts.py", base_name)
        run("step_video.py", base_name)
        archive_srt(base_name)
        clean_temp()

    print("\n✅ Rekonstruktion aller SRT-Dateien abgeschlossen.")

def select_speaker():
    from TTS.api import TTS

    model_name = "tts_models/en/vctk/vits"
    temp_dir = CONFIG.get("temp_dir", "temp")
    os.makedirs(temp_dir, exist_ok=True)

    print("🔊 Lade Modell zur Stimmvorschau...")
    tts = TTS(model_name=model_name, progress_bar=False, gpu=False)

    print("\n🎙️ Verfügbare Stimmen:")
    for idx, speaker in enumerate(tts.speakers):
        print(f"  [{idx+1}] {speaker}")

    while True:
        choice = input("\n🔍 Vorschau anhören? Nummer oder 'weiter': ").strip().lower()
        if choice in ['weiter', 'w', '']:
            break
        try:
            i = int(choice) - 1
            if 0 <= i < len(tts.speakers):
                speaker = tts.speakers[i]
                preview_file = os.path.join(temp_dir, f"_preview_{speaker}.wav")
                tts.tts_to_file(text="This is a voice test preview.", file_path=preview_file, speaker=speaker)
                subprocess.run(["afplay", preview_file])
        except Exception as e:
            print("⚠️ Fehler bei der Vorschau:", e)

    while True:
        selected = input("\n✅ Nummer der gewünschten Stimme: ").strip()
        try:
            idx = int(selected) - 1
            if 0 <= idx < len(tts.speakers):
                selected_speaker = tts.speakers[idx]
                break
        except:
            print("❌ Ungültige Eingabe.")

    config_path = "video_config.py"
    with open(config_path, "r") as f:
        lines = f.readlines()

    with open(config_path, "w") as f:
        for line in lines:
            if "default_speaker" in line:
                f.write(f'    "default_speaker": "{selected_speaker}",\n')
            else:
                f.write(line)

    print(f"\n✅ Stimme '{selected_speaker}' gespeichert.")

def menu():
    while True:
        print("\n🎬 AI Video Menü")
        print("1️⃣  Transkription (Whisper)")
        print("2️⃣  Glossar anwenden")
        print("3️⃣  Sprachclips erzeugen (Coqui TTS)")
        print("4️⃣  Neues Video bauen")
        print("5️⃣  ALLES ausführen (1 → 2 → 3 → 4)")
        print("6️⃣  🔁 Alle Videos im Ordner 'input/' verarbeiten")
        print("7️⃣  🔊 Stimme auswählen und speichern")
        print("8️⃣  🧹 Temp-Dateien löschen")
        print("9️⃣  ♻️ Neu-Kodierung aller vorhandenen SRTs")
        print("🔄 10️⃣  Rekonstruktion aus vorhandenen SRT-Dateien (in /temp)")
        print("0️⃣  Beenden")

        choice = input("\nWas möchtest du tun? ➤ ").strip()

        if choice == "1":
            base = input("🎞️ Basis-Dateiname (ohne .mp4): ").strip()
            run("step_transcribe.py", base)
            archive_srt(base)
        elif choice == "2":
            base = input("📜 Basis-Dateiname: ").strip()
            run("apply_glossary.py", base)
        elif choice == "3":
            base = input("🗣️ Basis-Dateiname: ").strip()
            run("step_tts.py", base)
        elif choice == "4":
            base = input("🎬 Basis-Dateiname: ").strip()
            run("step_video.py", base)
        elif choice == "5":
            base = input("🚀 Basis-Dateiname: ").strip()
            run("step_transcribe.py", base)
            run("apply_glossary.py", base)
            archive_srt(base)
            run("step_tts.py", base)
            run("step_video.py", base)
        elif choice == "6":
            process_bulk()
        elif choice == "7":
            select_speaker()
        elif choice == "8":
            clean_temp()
        elif choice == "9":
            reencode_existing()
        elif choice == "10":
            rebuild_from_existing_srt()
        elif choice == "0":
            print("👋 Tschüss!")
            break
        else:
            print("❌ Ungültige Eingabe.")

if __name__ == "__main__":
    menu()
