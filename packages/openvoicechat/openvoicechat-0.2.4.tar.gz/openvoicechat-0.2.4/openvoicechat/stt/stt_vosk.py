import numpy as np
import json

if __name__ == "__main__":
    from base import BaseEar
else:
    from .base import BaseEar


class Ear_vosk(BaseEar):
    def __init__(
        self, model_path="models/vosk-model-en-us-0.22", device="cpu", silence_seconds=2
    ):
        super().__init__(silence_seconds)
        import vosk

        self.model = vosk.Model(model_path)
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
        self.device = device

    def transcribe(self, audio):
        # if audio is a tensor convert it to numpy array
        audio = audio.astype(np.float64) * (1 << 15)
        audio = audio.astype(np.int16).tobytes()
        result_text = ""
        i = 0
        while True:
            data = audio[i * 12000 : (i + 1) * 12000]
            i += 1
            if len(data) == 0:
                break
            if self.recognizer.AcceptWaveform(data):
                if result_text == "":
                    result_text = json.loads(self.recognizer.Result())["text"]
                else:
                    result_text += json.loads(self.recognizer.Result())["text"]
            else:
                pass

        return result_text


if __name__ == "__main__":
    import torchaudio
    import torchaudio.functional as F

    ear = Ear_vosk(model_path="../models/vosk-model-en-us-0.22")

    audio, sr = torchaudio.load("../media/abs.wav")
    audio = F.resample(audio, sr, 16_000)[0]
    text = ear.transcribe(np.array(audio))
    print(text)

    text = ear.listen()
    print(text)
