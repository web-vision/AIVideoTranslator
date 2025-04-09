#!/bin/bash

echo "🚀 Starte Setup für AI Video Voiceover Projekt"

# Exit bei Fehlern
set -e

# Virtuelle Umgebung erstellen
echo "📦 Erstelle virtuelle Python-Umgebung..."
python3 -m venv venv
source venv/bin/activate

# Pip upgraden
pip install --upgrade pip

# FFmpeg Installation prüfen
if ! command -v ffmpeg &> /dev/null; then
    echo "🔧 ffmpeg wird über Homebrew installiert..."
    brew install ffmpeg
else
    echo "✅ ffmpeg ist bereits installiert."
fi

# Kompatible Torch-Version (2.0.1 für Bark)
echo "📦 Installiere kompatibles PyTorch (2.0.1)..."
pip install torch==2.0.1 torchvision torchaudio

# Whisper (direkt von GitHub)
echo "🧠 Installiere Whisper..."
pip install git+https://github.com/openai/whisper.git

# Bark + Abhängigkeiten
echo "🐶 Installiere Bark + SciPy..."
pip install git+https://github.com/suno-ai/bark.git
pip install scipy

# Coqui TTS + weitere Tools
echo "🗣️ Installiere Coqui TTS und pysrt..."
pip install TTS pysrt

# Arbeitsverzeichnisse erstellen
echo "📁 Lege Arbeitsverzeichnisse an..."
mkdir -p input output temp subtitles dictionary

# Wörterbücher herunterladen
echo "📚 Lade öffentlich verfügbare Wörterbücher herunter..."

curl -s -L -o dictionary/german.dic \
  https://raw.githubusercontent.com/wooorm/dictionaries/main/dictionaries/de/index.dic

curl -s -L -o dictionary/english.dic \
  https://raw.githubusercontent.com/wooorm/dictionaries/main/dictionaries/en/index.dic

echo "✅ Wörterbücher gespeichert in: dictionary/"

echo ""
echo "✅ Setup abgeschlossen!"
echo ""
echo "👉 Aktiviere die Umgebung mit:"
echo "   source venv/bin/activate"
echo ""
echo "📁 Danach kannst du dein Skript starten mit:"
echo "   python main_menu.py"