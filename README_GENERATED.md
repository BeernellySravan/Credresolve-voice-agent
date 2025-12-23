# CredResolve Voice Agent 🇮🇳

A simple Telugu voice assistant that provides guidance about government welfare schemes. It uses a small agent pipeline (plan → execute → evaluate) and supports speech-to-text (STT) and text-to-speech (TTS) in Telugu.

---

##  Project Overview

- Purpose: Help users ask questions about government schemes (రాష్ట్ర/కేంద్ర పథకాలు) in Telugu and get spoken answers.
- Core idea: Convert voice to text, use a lightweight planner to decide whether to check eligibility or answer general questions, then respond via TTS.
- Language: Telugu (te / te-IN locale for speech recognition)

---

##  Requirements

See `requirements.txt`. Key dependencies:

- Python 3.8+
- openai (optional / not yet used directly in core flow)
- whisper (optional)
- torch (optional for models)
- gTTS (TTS)
- pyaudio (microphone capture)
- SpeechRecognition (STT via Google Web Speech API)

Install in a venv:

```bash
python -m venv venv
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

Note: `gTTS` and `SpeechRecognition` use online services (Google) so internet is required for best results.

---

## ▶ Quick Start (Run)

1. Ensure microphone and speakers work on your system.
2. Run:

```bash
python main.py
```

3. The app will speak a welcome message (Telugu). Press ENTER to enable the microphone and speak your question. Press ENTER again after talking to stop.

Commands recognized (examples):
- Ask general questions about schemes (e.g., "రైతులకు ఏ పథకాలు ఉన్నారు?")
- Say "చాలు" to exit.

---

##  High-level Architecture

- `main.py` — Entry point. Handles TTS/ STT, keeps a `Memory`, and runs the agent loop.
- `agent/` — Small planning-execution-evaluation pipeline.
  - `memory.py` — Simple key/value store for short-term memory.
  - `planner.py` — Decides whether question requires eligibility check or a QA answer.
  - `executor.py` — Calls tools depending on the planner outcome.
  - `evaluator.py` — Post-processes and returns the final answer (currently identity).
  - `questions.py` — A small set of templated question/answer pairs (Telugu)
- `tools/` — Support tools
  - `tools.py` — Implements `qa_tool` (fuzzy matching against `data/qa_dataset.py`) and a simplified `eligibility_tool` that checks memory.
  - `eligibility_checker.py` — Function to match a user profile against `tools/scheme_db.py` scheme criteria.
  - `scheme_db.py` — Minimal scheme database listing schemes and eligibility criteria.
- `speech/` — Speech input/output utilities
  - `stt.py` — `speech_to_text_push_to_talk()` uses `speech_recognition` (Google) with push-to-talk steps.
  - `tts.py` — `speak()` uses `gTTS` to synthesize Telugu speech and plays it using Windows `start /wait`.
- `utils/` — Helper utilities
  - `audio.py` — `record_audio()` wrapper around `speech_recognition`.
- `data/` — Small QA dataset (`qa_dataset.py`) used by `qa_tool`.

---

##  Per-file Summary (what's inside & how to extend)

### `main.py` 
- Flow: welcome TTS → loop → STT → planner → executor → evaluator → TTS.
- To extend: adjust the `plan()` logic, add actions, or add more tools to the `tools` dict.

### `agent/questions.py` 
- Provides `QUESTIONS` — a list mapping keywords to answers for quick templated responses.
- To extend: add more entries with `keywords` and `answer` (Telugu).

### `agent/planner.py` 
- Very small rule-based planner: checks for keywords like "అర్హత" or "రైతు" and returns an action.
- To extend: replace rule-based logic with a classifier or large language model.

### `agent/memory.py` 
- Simple dict-based store with `update()` and `get()`.
- Use to store user info (occupation, has_children, etc.).

### `agent/executor.py` 
- Calls `eligibility` or `qa` tools based on action.
- To extend: add more actions and map them to additional tool calls.

### `agent/evaluator.py` 
- Currently passes the tool response through unchanged. Hook ML-based re-ranking or validation here.

### `tools/tools.py` 
- `qa_tool(user_text)` — fuzzy matches user_text to question in `QA_DATASET` using `SequenceMatcher` and returns answer if similarity > 0.5.
- `eligibility_tool(memory)` — example: if `occupation == "farmer"`, returns farmer schemes; otherwise asks for more details.
- To extend: use `eligibility_checker.check_eligibility()` with a filled user profile.

### `tools/scheme_db.py` 
- A small list `SCHEMES` with `name`, `category`, and `criteria` mapping keys to required values.
- Extend by adding scheme entries and richer criteria.

### `tools/eligibility_checker.py` 
- `check_eligibility(user_profile)` returns a list of scheme names where all `criteria` match the `user_profile`.

### `speech/stt.py` 
- `speech_to_text_push_to_talk()` uses `speech_recognition.Recognizer()` and google recognition (`language='te-IN'`).
- It uses simple input() prompts for push-to-talk control.
- Note: Errors return empty string.

### `speech/tts.py` 
- `speak(text)` uses `gTTS` with `lang='te'` and saves `output.mp3`, then plays using `start /wait output.mp3` (Windows).
- Keep in mind `gTTS` needs internet access.

### `utils/audio.py` 
- `record_audio()` — wrapper around `sr.Recognizer()` and `Microphone()` to capture raw audio object.

### `data/qa_dataset.py` 
- Contains `QA_DATASET` with Telugu Q/A pairs used by `qa_tool`.
- To improve coverage: add more question variants and synonyms.

---

##  Usage Tips & Known Limitations

- STT uses Google Web Speech and may require good internet connection and a clear mic.
- `gTTS` requires internet. If you need offline TTS, consider pyttsx3 or another local model.
- The fuzzy QA matching is basic; consider embedding-based similarity for better results.
- The eligibility logic is simplistic; integrate `eligibility_checker.check_eligibility()` and prompt for user profile fields when needed.

---

##  Ideas & Next Steps (TODOs)

- [ ] Replace rules with a small NLP classifier (intent detection).
- [ ] Improve QA matching with embeddings (sentence-transformers).
- [ ] Add an interactive flow to ask follow-up questions to build `user_profile` for eligibility.
- [ ] Unit tests and CI.
- [ ] Add a configuration file for locale and audio playback command.

---

##  Example Interaction (Telugu)

1. App speaks: "నమస్తే!..."
2. User: "రైతులకు ఏ పథకాలు ఉన్నారు?"
3. App: Looks up `QA_DATASET` and replies: "రైతుల కోసం రైతు భరోసా, పీఎం కిసాన్ వంటి పథకాలు ఉన్నాయి." (spoken via TTS)
