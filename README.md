# InclusiVoice Prototype

InclusiVoice is a desktop accessibility prototype for virtual interviews. It helps users with speech or communication difficulties by providing:

- Live interview question transcript (prototype stream)
- Context-aware response suggestions
- Editable response drafting
- Optional text-to-speech playback
- Non-intrusive topmost overlay interface with panic hide

## Project Structure

- `app.py` — entry point
- `inclusivoice/audio.py` — audio ingestion abstraction + simulated stream
- `inclusivoice/stt.py` — speech-to-text service interface (prototype pass-through)
- `inclusivoice/nlp.py` — question classification + response generation
- `inclusivoice/tts.py` — TTS service (pyttsx3 optional)
- `inclusivoice/ui.py` — Tkinter desktop overlay UI
- `tests/test_nlp.py` — basic NLP unit tests
- `InclusiVoice_Technical_Spec.md` — full technical case study specification

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then click **Start Simulated Interview** to run the end-to-end prototype flow.

## Notes

- This prototype uses simulated interview input for deterministic testing.
- `pyttsx3` is optional at runtime; if unavailable, the app still runs without voice output.
- For production, replace simulated ingestion with platform loopback capture and streaming ASR.

## Testing

```bash
python -m pytest -q
```
