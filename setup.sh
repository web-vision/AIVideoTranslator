#!/bin/bash

echo "🚀 Starte Setup für AI Video Voiceover Projekt"
set -e

# 🧹 Alte virtuelle Umgebung bereinigen
if [ -d "venv" ]; then
  echo "🧽 Entferne vorhandene virtuelle Umgebung..."
  deactivate 2>/dev/null || true
  rm -rf venv
fi

# 📦 Neue virtuelle Umgebung erstellen
echo "📦 Erstelle neue virtuelle Python-Umgebung..."
python3 -m venv venv
source venv/bin/activate

# 🆙 Pip aktualisieren
pip install --upgrade pip

# 🔧 FFmpeg Installation prüfen
if ! command -v ffmpeg &> /dev/null; then
    echo "🔧 ffmpeg wird über Homebrew installiert..."
    brew install ffmpeg
else
    echo "✅ ffmpeg ist bereits installiert."
fi

# 🔤 Hunspell CLI installieren
if ! command -v hunspell &> /dev/null; then
    echo "🔤 Installiere Hunspell über Homebrew..."
    brew install hunspell
else
    echo "✅ Hunspell ist bereits installiert."
fi

echo "✅ Hunspell CLI wird verwendet (kein Python-Binding notwendig)"

# 📥 Wörterbuch (Deutsch) von LibreOffice laden
echo "🌍 Lade deutsches Hunspell-Wörterbuch von GitHub..."
mkdir -p dictionary/libreoffice
curl -L -o dictionary/libreoffice/de_DE_frami.dic https://raw.githubusercontent.com/LibreOffice/dictionaries/master/de/de_DE_frami.dic
curl -L -o dictionary/libreoffice/de_DE_frami.aff https://raw.githubusercontent.com/LibreOffice/dictionaries/master/de/de_DE_frami.aff

echo "✅ Wörterbuch-Dateien heruntergeladen."

# 📦 Weitere Python-Tools
echo "📦 Installiere benötigte Python-Pakete..."
pip install git+https://github.com/openai/whisper.git
pip install pysrt

# 📁 Projektordner anlegen
mkdir -p input output temp subtitles dictionary hunspell_dicts

echo ""
echo "📘 Hinweis:"
echo "👉 Um alle Wortformen zu generieren, verwende:"
echo "   python expand_hunspell_cli.py"
echo "📁 Ausgabe: dictionary/german_expanded.dic"
echo ""
echo "✅ Setup abgeschlossen!"
echo "👉 Aktiviere die Umgebung mit: source venv/bin/activate"
echo "▶️  Starte dann mit: python main_menu.py"