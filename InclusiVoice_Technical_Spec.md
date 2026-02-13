# InclusiVoice — Technical Specification (Prototype)

## 1) Purpose and Scope

**InclusiVoice** is a desktop accessibility assistant for users with speech impediments or communication difficulties during virtual interviews. The prototype supports private, real-time question understanding and response assistance while preserving user control and confidentiality.

### 1.1 Goals
- Capture interview audio in real time from the user’s machine.
- Convert spoken interviewer questions into text with low latency.
- Generate context-aware response suggestions the user can edit/select.
- Provide optional text-to-speech (TTS) playback of user-approved responses.
- Remain private to the user through a local accessibility overlay (not visible in shared screens/meeting participants where feasible).

### 1.2 Non-goals (Prototype)
- Fully autonomous answering without user review.
- Guaranteed compatibility with every meeting platform and operating system policy.
- Clinical speech therapy outcomes.

---

## 2) Stakeholders and Primary User Stories

### 2.1 Stakeholders
- Primary: Job candidates with speech or communication disabilities.
- Secondary: Accessibility researchers, university evaluators, assistive-tech developers.

### 2.2 Core User Stories
1. As a candidate, I want live transcription of interviewer questions so I can process prompts accurately.
2. As a candidate, I want concise response suggestions tailored to interview context so I can answer confidently.
3. As a candidate, I want to approve/edit a response before speaking or TTS playback so I stay in control.
4. As a candidate, I want the tool to remain private and unobtrusive so I can use it discreetly.

---

## 3) System Context and High-Level Architecture

## 3.1 Deployment Model
- **Client-only first architecture** (recommended for prototype ethics/privacy):
  - Core pipeline runs locally on desktop.
  - Optional cloud NLP mode can be enabled explicitly for better model quality.

## 3.2 Logical Components
1. **Audio Ingestion Layer**
   - Captures system loopback audio (interviewer voice) and optional microphone reference.
2. **Speech Recognition Service**
   - Streaming ASR with partial/final transcript emission.
3. **Dialogue Intelligence Service**
   - Question detection, intent tagging, role/context memory, suggestion generation.
4. **Response Orchestration Layer**
   - Ranks suggestions, enforces safety filters, exposes candidate responses.
5. **TTS Service**
   - Converts user-confirmed text to natural speech.
6. **Overlay UI Client**
   - Accessibility-first interface always-on-top or docked panel.
7. **Security & Consent Layer**
   - Encryption, data retention controls, local audit events.

## 3.3 Data Flow (Real-Time)
1. Loopback/system audio frames (10–30 ms) captured.
2. Preprocessing: noise reduction, VAD, normalization.
3. Streaming ASR produces partial transcript.
4. Segment finalized by silence/endpointer.
5. NLP classifies as question type + context.
6. Suggestion engine returns 2–5 candidate responses.
7. User selects/edits response.
8. Optional TTS playback after explicit activation.

Target end-to-end latency from question end to first suggestion: **< 1.5 s** (stretch: < 1.0 s).

---

## 4) Audio Capture and Processing Architecture

## 4.1 OS Audio Capture
- **Windows**: WASAPI loopback capture.
- **macOS**: CoreAudio with virtual device support (e.g., AVAudioEngine + aggregate/virtual input).
- **Linux**: PulseAudio/PipeWire monitor sources.

## 4.2 Capture Modes
- **Primary mode**: system loopback capture for interviewer audio.
- **Fallback mode**: microphone-only if loopback unavailable.
- **Hybrid mode**: dual-channel capture for diarization (interviewer vs user).

## 4.3 Signal Processing Pipeline
- Sample rate: 16 kHz (ASR baseline), optional 24 kHz for higher-fidelity models.
- Frame size: 20 ms.
- Modules:
  - Automatic gain normalization.
  - RNNoise/WebRTC NS for denoising.
  - Voice Activity Detection (WebRTC VAD/Silero VAD).
  - Echo cancellation (if mic + speaker leakage occurs).

## 4.4 Performance Constraints
- CPU budget (prototype laptop): < 30% sustained for full pipeline.
- Memory footprint: < 1.2 GB in local-model mode.
- Audio drop tolerance: < 0.5% dropped frames over 30 min call.

---

## 5) Speech Recognition Integration

## 5.1 ASR Requirements
- Streaming inference with incremental transcripts.
- Domain adaptation for interview vocabulary (behavioral/technical terms).
- Word-level timestamps.
- Confidence scores per segment/token.

## 5.2 Candidate Engines
- **Offline/local**: faster-whisper (CTranslate2), Vosk, Whisper.cpp.
- **Cloud optional**: Azure Speech, Google STT, Deepgram.

## 5.3 Recommended Prototype Choice
- Default local engine: **faster-whisper small.en or medium.en** with dynamic model switching:
  - small model for low-spec hardware / low latency.
  - medium model when GPU available.

## 5.4 Error Handling
- Low-confidence transcript triggers:
  - visual uncertainty highlight,
  - request for repeat (optional prompt template),
  - reduced confidence weighting in suggestion model.

---

## 6) NLP and Context-Aware Response Generation

## 6.1 Functional Objectives
- Identify whether transcript is an interview question.
- Classify question type:
  - behavioral (STAR),
  - technical explanation,
  - experience/background,
  - situational/conflict,
  - logistics/salary/availability.
- Generate concise, professional draft responses.

## 6.2 NLP Pipeline
1. **Utterance segmentation** from ASR stream.
2. **Question detection** (classifier + punctuation/prosody cues).
3. **Intent/category classification** (lightweight transformer or rules+ML hybrid).
4. **Context retrieval** from session memory:
   - user profile snippets,
   - CV highlights,
   - role description,
   - previous answered questions.
5. **Response generation** (LLM or local NLG model).
6. **Post-processing**:
   - length control,
   - readability optimization,
   - toxicity/safety checks,
   - bias-sensitive filter.

## 6.3 Suggestion Strategy
- Provide 3 tiers:
  1. **Quick reply (1 sentence)**,
  2. **Standard answer (3–5 sentences)**,
  3. **STAR structured answer**.
- Include key talking points bullets before full text.

## 6.4 Model Options
- **Local-first**:
  - classifier: DistilBERT/MiniLM.
  - generator: quantized 3B–8B instruct model (if hardware permits).
- **Hybrid/cloud**:
  - API LLM with strict redaction and consent gates.

## 6.5 Guardrails
- Never auto-send/speak generated text.
- Prominent indicator: “AI Draft — Review Before Use.”
- Block or warn for fabricated credentials/experience claims.

---

## 7) Text-to-Speech (TTS) Engine Specification

## 7.1 TTS Requirements
- Natural, intelligible output.
- Latency from click-to-speech start: < 400 ms target.
- Voice personalization options (pitch/rate/voice style).
- Offline fallback voice.

## 7.2 Candidate Engines
- OS-native:
  - Windows SAPI,
  - macOS AVSpeechSynthesizer,
  - Linux Speech Dispatcher.
- Neural:
  - Coqui TTS (local),
  - Azure Neural Voices / ElevenLabs (cloud; consent-based).

## 7.3 Playback Controls
- Push-to-speak hotkey (default disabled).
- Pre-play preview (silent read mode).
- Emergency mute/stop hotkey.
- Output routing selector (virtual mic vs speakers per policy).

## 7.4 Accessibility Features
- Adjustable speech rate (0.6x–1.4x).
- Phrase chunking for breath pacing.
- Optional dysfluency-aware pausing templates.

---

## 8) UI/UX and Accessibility Requirements

## 8.1 Design Principles
- Non-intrusive, minimal cognitive load.
- Keyboard-first and screen-reader compatible.
- High-contrast themes and scalable typography.

## 8.2 Overlay Behavior
- Always-on-top compact widget with expandable panel.
- Configurable transparency and docking.
- “Private Mode” attempts to avoid capture in screen-share:
  - use separate window layer/API where OS allows,
  - explicit warning that behavior depends on conferencing platform.

## 8.3 Primary UI Elements
- Live transcript pane.
- Suggestion cards with confidence indicators.
- Edit box with readability meter.
- TTS action button (disabled until consent toggle on).
- Session status bar: mic/system capture/latency/privacy flags.

## 8.4 Interaction Shortcuts
- Hotkeys:
  - Toggle overlay,
  - Next/previous suggestion,
  - Insert template,
  - Trigger TTS,
  - Panic hide.
- Full remapping for motor accessibility needs.

## 8.5 Inclusive UX Considerations
- Low-vision mode.
- Simplified language mode.
- Multi-lingual support roadmap.
- Minimize flashing/animation.

---

## 9) Privacy, Security, and Compliance Controls

## 9.1 Privacy-by-Design Baseline
- Default: no cloud upload, local processing only.
- Data minimization: process only active-call audio.
- Session-local memory with auto-expiry.

## 9.2 Consent and Transparency
- First-run consent flow explaining:
  - what audio is captured,
  - where processing occurs,
  - retention settings,
  - user rights and deletion.
- Explicit user action required before TTS output.

## 9.3 Data Retention Policy (Prototype)
- Transcript storage default: off.
- If enabled by user:
  - encrypted local store,
  - retention window (e.g., 24h/7d/custom),
  - one-click purge.

## 9.4 Security Controls
- At rest encryption: AES-256 for local artifacts.
- In transit encryption (cloud mode): TLS 1.2+.
- Secret management: OS keychain/credential vault.
- Signed updates and binary integrity checks.

## 9.5 Interview Ethics & Policy Notes
- Include visible notice in app settings regarding local legal requirements for recording/transcription consent.
- No covert broadcasting, remote monitoring, or auto-join meeting behavior.

---

## 10) Functional Requirements (FR)

- **FR-01**: System shall capture system audio with < 100 ms buffering delay.
- **FR-02**: System shall display partial ASR text during active speech.
- **FR-03**: System shall generate at least 2 response suggestions per detected question.
- **FR-04**: System shall allow user editing before TTS activation.
- **FR-05**: System shall require explicit per-response TTS trigger.
- **FR-06**: System shall provide panic hide within 100 ms.
- **FR-07**: System shall support keyboard-only operation.
- **FR-08**: System shall expose privacy settings and clear session data on demand.

## 11) Non-Functional Requirements (NFR)

- **NFR-01 (Latency)**: Question-end to first suggestion < 1.5 s (p95).
- **NFR-02 (Reliability)**: 99% session uptime across 60-minute run.
- **NFR-03 (Usability)**: SUS score target >= 75 in pilot evaluation.
- **NFR-04 (Accessibility)**: WCAG 2.2 AA-aligned visual contrast and navigation.
- **NFR-05 (Security)**: No plaintext storage of transcripts when persistence enabled.

---

## 12) Prototype Technology Stack (Suggested)

## 12.1 Desktop Framework
- **Primary**: Electron + TypeScript (rapid UI iteration).
- **Alternative**: Tauri + Rust (lower footprint).

## 12.2 Core Services
- Audio service: Rust/Go native module for stable low-latency capture.
- ASR/NLP/TTS orchestration: Python microservice (FastAPI + local IPC) or Rust service.
- IPC: gRPC over localhost / Unix domain socket / named pipe.

## 12.3 Storage
- SQLite (encrypted extension) for optional session artifacts.
- JSON config in user profile directory with secure defaults.

## 12.4 Observability
- Structured local logs with PII redaction.
- Performance telemetry opt-in only.
- Crash reporting disabled by default unless consented.

---

## 13) API and Internal Interfaces (Prototype)

## 13.1 Event Bus Topics
- `audio.frame`
- `asr.partial`
- `asr.final`
- `nlp.question_detected`
- `nlp.suggestions_ready`
- `tts.play_request`
- `security.consent_changed`

## 13.2 Sample IPC Contracts
```json
{
  "event": "asr.final",
  "timestamp": "2026-02-13T10:10:10Z",
  "text": "Can you describe a time you handled conflict in a team?",
  "confidence": 0.91,
  "segment_id": "seg_204"
}
```

```json
{
  "event": "nlp.suggestions_ready",
  "segment_id": "seg_204",
  "question_type": "behavioral_conflict",
  "suggestions": [
    {"id":"s1","style":"quick","text":"I address conflict by clarifying goals and aligning on facts first."},
    {"id":"s2","style":"star","text":"Situation: ... Task: ... Action: ... Result: ..."}
  ]
}
```

---

## 14) Risk Register and Mitigations

1. **ASR errors in noisy meetings**
   - Mitigation: denoising + confidence UI + quick correction shortcuts.
2. **Model hallucination in responses**
   - Mitigation: guardrails + user review + factuality prompts.
3. **Overlay visibility in screen share**
   - Mitigation: platform-specific private window handling + warnings.
4. **Ethical/legal misuse concerns**
   - Mitigation: consent UX + transparent policy + no autonomous actions.

---

## 15) Validation Plan for Case Study

## 15.1 Technical Validation
- Measure p50/p95 latency across 30 simulated interview questions.
- WER benchmark on interview audio corpus.
- TTS intelligibility rating test.

## 15.2 Human Factors Evaluation
- 8–15 participant pilot with accessibility needs.
- Metrics:
  - NASA-TLX (cognitive load),
  - SUS (usability),
  - perceived confidence before/after tool use,
  - qualitative comfort/privacy feedback.

## 15.3 Success Criteria
- >= 20% reduction in response preparation time.
- >= 15-point improvement in perceived interview confidence (self-report scale).
- No critical privacy violations in audit checklist.

---

## 16) Prototype Roadmap

### Phase 1 (MVP, 4–6 weeks)
- Local audio capture + streaming ASR + transcript UI.

### Phase 2 (4 weeks)
- Question classification + suggestion generation + editable responses.

### Phase 3 (3 weeks)
- TTS integration + privacy/consent controls + hotkeys.

### Phase 4 (2–3 weeks)
- Pilot testing, logging analysis, accessibility refinements.

---

## 17) Research Deliverables

- Architecture diagram and threat model.
- Working desktop prototype.
- Evaluation report with quantitative and qualitative findings.
- Ethical reflection on assistive AI in hiring workflows.

