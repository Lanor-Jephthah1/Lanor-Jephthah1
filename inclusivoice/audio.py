from __future__ import annotations

import queue
import threading
import time
from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class AudioConfig:
    chunk_ms: int = 250
    sample_rate: int = 16000


class AudioCaptureService:
    """Prototype audio capture service.

    Real loopback/mic capture is platform-specific; for prototype speed this service
    supports a simulation mode that emits text-like "audio events" into the pipeline.
    Replace `start_simulated_stream` with real PCM callbacks in production.
    """

    def __init__(self, config: Optional[AudioConfig] = None) -> None:
        self.config = config or AudioConfig()
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self.events: "queue.Queue[str]" = queue.Queue()

    def start_simulated_stream(self, script: list[str], delay_s: float = 2.0) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()

        def _run() -> None:
            for item in script:
                if self._stop.is_set():
                    break
                self.events.put(item)
                time.sleep(delay_s)

        self._thread = threading.Thread(target=_run, daemon=True)
        self._thread.start()

    def poll(self, timeout: float = 0.1) -> Optional[str]:
        try:
            return self.events.get(timeout=timeout)
        except queue.Empty:
            return None

    def stop(self) -> None:
        self._stop.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)


def default_interview_script() -> list[str]:
    return [
        "Can you tell me about yourself and your background?",
        "Describe a time you handled conflict in a team.",
        "Why are you interested in this role?",
        "What is one technical challenge you solved recently?",
    ]
