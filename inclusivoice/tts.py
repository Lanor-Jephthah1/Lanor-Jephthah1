from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TTSConfig:
    rate: int = 180
    enabled: bool = True


class TextToSpeechService:
    def __init__(self, config: TTSConfig | None = None) -> None:
        self.config = config or TTSConfig()
        self._engine = None
        if self.config.enabled:
            try:
                import pyttsx3  # type: ignore

                self._engine = pyttsx3.init()
                self._engine.setProperty("rate", self.config.rate)
            except Exception:
                self._engine = None

    def speak(self, text: str) -> bool:
        if not text.strip():
            return False
        if self._engine is None:
            return False
        self._engine.say(text)
        self._engine.runAndWait()
        return True
