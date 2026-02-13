from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TranscriptSegment:
    text: str
    confidence: float


class SpeechToTextService:
    """Prototype STT service.

    In this MVP, incoming events are already text and are passed through as final
    transcript segments. This keeps the architecture clear while allowing immediate
    prototype interaction and testing.
    """

    def transcribe(self, audio_event: str) -> TranscriptSegment:
        cleaned = audio_event.strip()
        confidence = 0.95 if cleaned.endswith("?") else 0.9
        return TranscriptSegment(text=cleaned, confidence=confidence)
