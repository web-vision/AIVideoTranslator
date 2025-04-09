import os
import sys
import re
import pysrt

from video_config import CONFIG
import importlib.util

TEMP_DIR = CONFIG.get("temp_dir", "temp")
DICT_DIR = "dictionary"

base_name = sys.argv[1] if len(sys.argv) > 1 else "default"
srt_path = os.path.join(TEMP_DIR, f"{base_name}_en.srt")

if not os.path.exists(srt_path):
    print("❌ SRT-Datei nicht gefunden.")
    exit(1)

# Lade Glossar (dynamisch)
spec = importlib.util.spec_from_file_location("glossary", "glossary.py")
glossary_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(glossary_module)
GLOSSARY = glossary_module.GLOSSARY

print("📘 Wende Glossar auf Textzeilen an...")
subs = pysrt.open(srt_path)

# Wörterbücher laden
def load_dictionary(filepath):
    if not os.path.exists(filepath):
        return set()
    with open(filepath, encoding="utf-8") as f:
        return set(word.strip().lower() for word in f if word.strip())

dictionary_words = load_dictionary(os.path.join(DICT_DIR, "german.dic")) | \
                   load_dictionary(os.path.join(DICT_DIR, "english.dic"))

# Vorschläge für Glossar sammeln
new_glossary_entries = {}

for sub in subs:
    original = sub.text
    text = sub.text

    # Bestehende Glossar-Ersetzungen
    for search, replacement in GLOSSARY.items():
        pattern = re.escape(search).replace(r"\*", ".*")
        regex = re.compile(r"\b" + pattern + r"\b", re.IGNORECASE)
        text = regex.sub(replacement, text)

    # Wörter extrahieren
    words = re.findall(r'\b\w+(?:\s+\w+)?\b', text)

    for word in words:
        if word.lower() not in dictionary_words:
            # Wenn zusammengesetzte Begriffe wie "Typo 3" → Vorschlag "Typo3"
            if " " in word:
                suggestion = word.replace(" ", "")
                if suggestion.lower() in dictionary_words:
                    new_glossary_entries[word] = suggestion

    sub.text = text

# Änderungen speichern
subs.save(srt_path, encoding="utf-8")
print("✅ Glossar-Anpassungen gespeichert.")

# Neue Glossar-Vorschläge in glossary.py eintragen
if new_glossary_entries:
    glossary_file = "glossary.py"
    with open(glossary_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Neueinträge ergänzen vor der letzten Klammer
    with open(glossary_file, "w", encoding="utf-8") as f:
        for line in lines:
            if line.strip() == "}":
                for key, val in new_glossary_entries.items():
                    f.write(f'    "{key}": "{val}",\n')
                f.write("}\n")
                break
            else:
                f.write(line)

    for key in new_glossary_entries:
        print(f"➕ Begriff \"{key}\" wurde dem Glossar hinzugefügt. Bitte Glossar überarbeiten.")

else:
    print("ℹ️ Keine neuen Begriffe für das Glossar gefunden.")