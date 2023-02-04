from pathlib import Path
import whisper
from typing import Optional


class TranscribeResult:

    def __init__(self, language: str, text: str):
        self.language = language
        self.text = text


class Transcriber:

    def __init__(self):
        self.model = whisper.load_model("base")

    def transcribe_from_file(self, file_path: Path, language: Optional[str] = None) -> TranscribeResult:

        audio = whisper.load_audio(str(file_path))
        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

        detected_lang = str()
        if language is None:
            _, probs = self.model.detect_language(mel)
            detected_lang = max(probs, key=probs.get)
        else:
            detected_lang = language

        # if language is None then whisper will auto-detect the language
        options = whisper.DecodingOptions(fp16=False, language=language)

        decoding_result = whisper.decode(self.model, mel, options)
        result = TranscribeResult(detected_lang, decoding_result.text)

        return result


transcriber = Transcriber()
