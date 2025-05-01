import os
import sys
import pysrt
import re
from importlib.util import spec_from_file_location, module_from_spec

# 🧾 Basisdateiname über Argument
if len(sys.argv) < 2:
    print("❌ Bitte gib den Basis-Dateinamen als Argument an. Beispiel:")
    print("   python apply_glossary.py 08-03-eigenes-preset")
    sys.exit(1)

base_name = sys.argv[1]

# 📖 Glossar importieren
glossary_file = "glossary.py"
if not os.path.exists(glossary_file):
    print("❌ glossary.py nicht gefunden.")
    sys.exit(1)

spec = spec_from_file_location("glossary", glossary_file)
glossary_module = module_from_spec(spec)
spec.loader.exec_module(glossary_module)

if not hasattr(glossary_module, "glossary"):
    print("❌ glossary.py enthält kein 'glossary = {...}' Dictionary.")
    sys.exit(1)

glossary = glossary_module.glossary
print(f"📑 Geladene Glossarbegriffe: {len(glossary)}")

# 🔁 Wende Glossar auf DE und EN SRT-Dateien an
for lang in ["de", "en"]:
    input_srt = f"subtitles/{base_name}_{lang}.srt"
    output_srt = f"subtitles/{base_name}_{lang}_glossed.srt"

    if not os.path.exists(input_srt):
        print(f"⚠️  Datei nicht gefunden: {input_srt}")
        continue

    print(f"📝 Verarbeite: {input_srt}")
    subs = pysrt.open(input_srt)
    changes = 0

    for sub in subs:
        original_text = sub.text

        # 🛠 Non-breaking Spaces ersetzen
        normalized_text = original_text.replace('\u00A0', ' ')

        new_text = normalized_text

        for key, replacement in glossary.items():
            pattern = re.compile(rf"\b{re.escape(key)}\b", re.IGNORECASE)
            new_text, count = pattern.subn(replacement, new_text)
            changes += count

        sub.text = new_text

    subs.save(output_srt, encoding='utf-8')
    print(f"✅ Gespeichert: {output_srt} ({changes} Ersetzungen)")