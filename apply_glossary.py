import os
import sys
import re
import pysrt
from glossary import GLOSSARY
from video_config import CONFIG

TEMP_DIR = CONFIG.get("temp_dir", "temp")
base_name = sys.argv[1] if len(sys.argv) > 1 else "default"
srt_path = os.path.join(TEMP_DIR, f"{base_name}_en.srt")

if not os.path.exists(srt_path):
    print("❌ SRT-Datei nicht gefunden.")
    exit(1)

print("📘 Wende Glossar auf Textzeilen an...")

subs = pysrt.open(srt_path)

for sub in subs:
    original = sub.text

    for search, replacement in GLOSSARY.items():
        pattern = re.escape(search).replace(r"\*", ".*")
        regex = re.compile(r"\b" + pattern + r"\b", re.IGNORECASE)
        sub.text = regex.sub(replacement, sub.text)

    if sub.text != original:
        print(f"🔁 Ersetzt: \"{original}\" → \"{sub.text}\"")

subs.save(srt_path, encoding="utf-8")
print("✅ Glossar erfolgreich angewendet.")
