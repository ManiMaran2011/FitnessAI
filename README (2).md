
---
title: FitnessAI
sdk: gradio
app_file: app.py
python_version: 3.10
---

# 💪 FitnessAI — AI‑Powered Fitness Planner

FitnessAI generates **personalized workout and meal plans** using OpenAI models,
and includes an **interactive chatbot** for fitness guidance.

## 🚀 Features
- Custom workout plan (7‑day split)
- Personalized meal plan (diet‑aware)
- Chatbot for follow‑up fitness questions
- Clean Gradio web UI (HuggingFace‑ready)

## ▶️ Running on HuggingFace
This Space auto-detects your `OPENAI_API_KEY` if added in:

**Settings → Secrets → Add new secret**

Name: `OPENAI_API_KEY`  
Value: your API key

## ▶️ Running locally
```bash
pip install -r requirements.txt
export OPENAI_API_KEY=yourkey
python app.py
```
