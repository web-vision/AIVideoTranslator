# AIVideo Translator

**AIVideo Translator** is an open-source project for automated video translation using artificial intelligence. It combines speech-to-text, machine translation, and text-to-speech technologies to efficiently transfer spoken content into other languages.

## Why this project and Big Kudos
I started this project to translate the great #TYPO3 traning videos which are produced and provided by [Wolfgang Wagner](https://wwagner.net/), but were only available in German. As we in web-vision are a team of people with multiple cultures and languages, we had the need to translate those videos to English. 

**Big Kudos** to Wolfgang Wagner for providing us with the videos, which we now can use for internal trainings of TYPO3 beginners. 


## 🌐 Features

- Transcription of spoken video audio
- Translation into multiple languages
- Output as a subtitled file or synthetic audio track
- Support for modern AI models (e.g., OpenAI Whisper, Transformers)
- Customizable dictionaries

---

## 🛠 System Requirements

- **Operating System**: Linux, macOS, or Windows 10+
- **Python**: Version 3.9 or higher
- **RAM**: Minimum 8 GB (recommended: 16 GB for large videos)
- **GPU**: Optional (for faster processing via CUDA)
- **ffmpeg**: Must be installed and available in the system PATH
- **pip**: Python Package Installer

---

## ⚙️ Setup Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/web-vision/aivideotranslator.git
    cd aivideotranslator
    ```

2. Create a virtual environment (optional, recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run an example:
    ```bash
    python translate.py --input video.mp4 --source-lang en --target-lang de
    ```

---

## 🍀 Hints
- You can use the extracted SRT-Files for providing sub-titles in various languages. Also, it's recommended to check them occasionally as sometimes special terms and phrase are not well translated. Correct them with any text editor you want.
- Use the glossary.py file to define various notations or even wrong spellings of brands or terms and phrases. Some exmaples for "TYPO3" are already included.
- Check the languages selection first. Some speakers sound more natural than others. We use "p230" which sounds like a native English speaker to us (at least for my German ears).
- You can configure some things, as the speaker or the type of subtitles you want to have  in the video_congfig.py


## 🧩 Open-Source Components Used

This project uses the following open-source libraries:

- [OpenAI Whisper](https://github.com/openai/whisper) – Speech-to-Text (MIT License)
- [transformers](https://github.com/huggingface/transformers) – Machine Translation (Apache 2.0)
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python) – Video and audio processing (MIT License)
- [gTTS](https://github.com/pndurette/gTTS) – Google Text-to-Speech (MIT License)

All listed components are **compatible with GPLv3**.

---

## ⚖️ Disclaimer

This project is provided **without any warranty**. Use at your own risk. The author assumes no liability for any damages, data loss, or other consequences resulting from the use of this software.

---

## 📜 License

This project is licensed under the **GNU General Public License Version 3 (GPLv3)**.  
For more information, see the [LICENSE](LICENSE) file or visit [https://www.gnu.org/licenses/gpl-3.0.en.html](https://www.gnu.org/licenses/gpl-3.0.en.html).

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📧 Contact

For questions or suggestions, feel free to reach out at [b.hinzer@web-vision.de].