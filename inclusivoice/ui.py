from __future__ import annotations

import threading
import tkinter as tk
from tkinter import ttk

from inclusivoice.audio import AudioCaptureService, default_interview_script
from inclusivoice.nlp import generate_suggestions
from inclusivoice.stt import SpeechToTextService
from inclusivoice.tts import TextToSpeechService


class InclusiVoiceApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("InclusiVoice (Prototype)")
        self.root.geometry("900x620")
        self.root.attributes("-topmost", True)

        self.audio = AudioCaptureService()
        self.stt = SpeechToTextService()
        self.tts = TextToSpeechService()

        self.current_text = tk.StringVar(value="Waiting for interview question...")
        self.current_type = tk.StringVar(value="Question type: -")
        self.quick = tk.StringVar(value="")

        self._build_ui()
        self._polling = False

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill="both", expand=True)

        title = ttk.Label(frame, text="InclusiVoice Accessibility Overlay", font=("Segoe UI", 14, "bold"))
        title.pack(anchor="w")

        ttk.Label(frame, text="Live Transcript", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 2))
        self.transcript = tk.Text(frame, height=6, wrap="word")
        self.transcript.pack(fill="x")
        self.transcript.insert("1.0", self.current_text.get())

        ttk.Label(frame, textvariable=self.current_type).pack(anchor="w", pady=(8, 4))

        ttk.Label(frame, text="Quick Suggestion", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        ttk.Label(frame, textvariable=self.quick, wraplength=860).pack(anchor="w", pady=(0, 8))

        ttk.Label(frame, text="Editable Response", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.editor = tk.Text(frame, height=10, wrap="word")
        self.editor.pack(fill="both", expand=True)

        controls = ttk.Frame(frame)
        controls.pack(fill="x", pady=(10, 0))

        ttk.Button(controls, text="Start Simulated Interview", command=self.start_simulation).pack(side="left")
        ttk.Button(controls, text="Speak Response", command=self.speak_response).pack(side="left", padx=8)
        ttk.Button(controls, text="Clear", command=self.clear_response).pack(side="left")
        ttk.Button(controls, text="Panic Hide", command=self.panic_hide).pack(side="right")

    def start_simulation(self) -> None:
        self.audio.start_simulated_stream(default_interview_script(), delay_s=4.0)
        if not self._polling:
            self._polling = True
            self.root.after(100, self.poll_audio)

    def poll_audio(self) -> None:
        event = self.audio.poll(timeout=0.01)
        if event:
            seg = self.stt.transcribe(event)
            self.transcript.delete("1.0", "end")
            self.transcript.insert("1.0", seg.text)

            suggestions = generate_suggestions(seg.text)
            self.current_type.set(f"Question type: {suggestions.question_type}")
            self.quick.set(suggestions.quick_reply)

            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", suggestions.standard_reply)

        if self._polling:
            self.root.after(100, self.poll_audio)

    def speak_response(self) -> None:
        text = self.editor.get("1.0", "end").strip()

        def _speak() -> None:
            self.tts.speak(text)

        threading.Thread(target=_speak, daemon=True).start()

    def clear_response(self) -> None:
        self.editor.delete("1.0", "end")

    def panic_hide(self) -> None:
        self.root.withdraw()
        self.root.after(2000, self.root.deiconify)

    def run(self) -> None:
        self.root.mainloop()


def run_app() -> None:
    InclusiVoiceApp().run()
