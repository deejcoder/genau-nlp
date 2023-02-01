from pathlib import Path
import whisper


class TranscribeResult:

    def __init__(self, language: str, text: str):
        self.language = language
        self.text = text


class Transcriber:

    def __init__(self):
        self.model = whisper.load_model("base")
        self.options = whisper.DecodingOptions(fp16=False)

    def transcribe_from_file(self, file_path: Path) -> TranscribeResult:

        audio = whisper.load_audio(str(file_path))
        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

        _, probs = self.model.detect_language(mel)

        decoding_result = whisper.decode(self.model, mel, self.options)
        result = TranscribeResult(max(probs, key=probs.get), decoding_result.text)

        return result
