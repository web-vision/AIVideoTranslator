#!/bin/bash

echo "📦 Lade deutsches Wörterbuch von LibreOffice (GitHub)..."

OUT_DIR="dictionary"
LO_DIR="$OUT_DIR/libreoffice"
URL_BASE="https://raw.githubusercontent.com/LibreOffice/dictionaries/master/de"
DICT_SRC="$LO_DIR/de_DE_frami.dic"
DICT_UTF="$LO_DIR/de_DE_frami.utf8.dic"
FINAL_FILE="$OUT_DIR/german.dic"

# 🛠 Verzeichnisse anlegen
mkdir -p "$LO_DIR"

# 📥 Wörterbuch herunterladen
echo "⏬ Lade de_DE_frami.dic ..."
curl -L -o "$DICT_SRC" "$URL_BASE/de_DE_frami.dic"

if [ ! -f "$DICT_SRC" ]; then
    echo "❌ Fehler: Wörterbuch konnte nicht heruntergeladen werden."
    exit 1
fi

# 🔁 Encoding umwandeln (nach UTF-8)
echo "🔁 Konvertiere Encoding nach UTF-8 ..."
iconv -f ISO-8859-1 -t UTF-8 "$DICT_SRC" > "$DICT_UTF"

# 🧹 Wörter extrahieren
echo "🧹 Extrahiere Wörter aus .dic ..."
tail -n +2 "$DICT_UTF" | cut -d '/' -f1 | awk '{print tolower($0)}' | sort | uniq > "$FINAL_FILE"

echo "✅ Wörterbuch erfolgreich erstellt:"
echo "📁 $FINAL_FILE"