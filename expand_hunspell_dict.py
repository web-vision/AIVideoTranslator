import os
import subprocess

DICT_SOURCE = "dictionary/libreoffice"
DICT_NAME = "de_DE_frami"
LOCAL_DICT_DIR = "hunspell_dicts"
OUTPUT_PATH = "dictionary/german_expanded.dic"
TMP_WORDS = "dictionary/_base_words.tmp"

# Sicherstellen, dass hunspell lokale Kopie nutzen kann
os.makedirs(LOCAL_DICT_DIR, exist_ok=True)
dic_copy = os.path.join(LOCAL_DICT_DIR, "de_DE.dic")
aff_copy = os.path.join(LOCAL_DICT_DIR, "de_DE.aff")

if not os.path.exists(dic_copy):
    os.system(f"cp {DICT_SOURCE}/{DICT_NAME}.dic {dic_copy}")
if not os.path.exists(aff_copy):
    os.system(f"cp {DICT_SOURCE}/{DICT_NAME}.aff {aff_copy}")

# Wörter extrahieren
with open(f"{DICT_SOURCE}/{DICT_NAME}.dic", "r", encoding="ISO-8859-1") as f:
    lines = f.readlines()[1:]
    words = sorted(set(line.split("/")[0].strip().lower() for line in lines))

# temporäre Datei schreiben
with open(TMP_WORDS, "w", encoding="utf-8") as f:
    f.write("\n".join(words))

print("📤 Basiswörter vorbereitet – Generiere Formen mit hunspell...")

# Hunspell ausführen
proc = subprocess.run(
    ["hunspell", "-d", "de_DE", "-m"],
    input="\n".join(words),
    text=True,
    capture_output=True,
    env={**os.environ, "DICPATH": LOCAL_DICT_DIR}
)

if proc.returncode != 0:
    print("❌ Fehler bei hunspell:", proc.stderr)
    exit(1)

# Ergebnisse parsen
forms = set()
for line in proc.stdout.splitlines():
    if line.strip():
        forms.update(line.split())

# Speichern
with open(OUTPUT_PATH, "w", encoding="utf-8") as out:
    for form in sorted(forms):
        out.write(form + "\n")

os.remove(TMP_WORDS)
print(f"✅ Erfolgreich gespeichert: {OUTPUT_PATH} ({len(forms)} Wortformen)")