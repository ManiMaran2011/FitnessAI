
# FitnessAI

**FitnessAI** is an AI-driven fitness recommendation system that generates personalized **workout** and **meal** plans from user parameters (height, weight, goals, preferences). It also includes an **interactive LLM-powered chatbot** for follow-up questions and real-time guidance.

## Features
- Personalized workout plans (with sets/reps, recovery, progression)
- AI-generated meal plans (diet-aware with macro guidance)
- Interactive chatbot for Q&A and plan adjustments
- Works as a simple CLI; supports arguments or interactive prompts

## Files
- `app.py` — main Python application (CLI)
- `requirements.txt` — Python dependencies
- `.env.example` — example of required environment variables

## Setup

### 1) Create & activate a virtual environment
```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Configure API key
Copy `.env.example` to `.env` and put your key:
```
OPENAI_API_KEY=sk-...
```
Then load it in your shell (optional if you export manually):
- macOS/Linux:
  ```bash
  export $(grep -v '^#' .env | xargs)
  ```
- Windows PowerShell:
  ```powershell
  Get-Content .env | ForEach-Object {
    if ($_ -match '^(.*?)=(.*)$') { $name=$matches[1]; $value=$matches[2]; [Environment]::SetEnvironmentVariable($name,$value,'Process') }
  }
  ```

Alternatively, set `OPENAI_API_KEY` directly in your environment.

## Run

### Interactive prompts
```bash
python app.py
```

### Non-interactive (headless) with arguments
```bash
python app.py --height_cm 178 --weight_kg 74 --age 24 --sex male --goal "muscle gain" --experience beginner --diet "non-veg" --constraints "no knee issues"
```

Add `--no_chat` if you only want the generated plan and to skip the chatbot.

## Notes
- The chatbot and plans use the `gpt-4o-mini` model by default (edit in `app.py` if needed).
- Internet connection is required for LLM calls.
- For a web demo (Hugging Face/Streamlit/Gradio), we can add a simple UI later.
