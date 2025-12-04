
import os
import gradio as gr
from openai import OpenAI

# Initialize OpenAI client
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

def generate_plan(height, weight, age, sex, goal, diet, experience):
    if not client:
        return "Error: OPENAI_API_KEY not set in HuggingFace Secrets.", "", ""

    prompt = f'''
You are a certified fitness and nutrition trainer.
Create a personalized fitness plan based on:

Height: {height} cm
Weight: {weight} kg
Age: {age}
Sex: {sex}
Goal: {goal}
Diet: {diet}
Experience: {experience}

Return two sections:
### Workout Plan
- 7 day routine with sets, reps, rest, and progression.

### Meal Plan
- 7 day meal plan with breakfast, lunch, dinner, snacks.
- Follow diet preference.
'''

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    full_output = resp.choices[0].message.content
    return full_output, "", ""

def chatbot(message, history):
    if not client:
        return "OPENAI_API_KEY not set."
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":"You are a fitness assistant."}] +
                [{"role":"user","content":message}],
        temperature=0.4
    )
    return resp.choices[0].message.content

with gr.Blocks() as demo:
    gr.Markdown("# 💪 FitnessAI — Personalized Workout & Meal Plans")

    with gr.Tab("Generate Plan"):
        height = gr.Number(label="Height (cm)")
        weight = gr.Number(label="Weight (kg)")
        age = gr.Number(label="Age")
        sex = gr.Dropdown(choices=["male","female","other"], label="Sex")
        goal = gr.Textbox(label="Goal (fat loss, muscle gain, etc.)")
        diet = gr.Textbox(label="Diet Preference (veg, non‑veg, vegan)")
        experience = gr.Dropdown(choices=["beginner","intermediate","advanced"], label="Experience Level")

        generate_btn = gr.Button("Generate Plan")
        workout_output = gr.Textbox(label="Workout & Meal Plan", lines=20)

        generate_btn.click(
            generate_plan,
            inputs=[height, weight, age, sex, goal, diet, experience],
            outputs=[workout_output, None, None]
        )

    with gr.Tab("Chatbot"):
        gr.Markdown("Ask follow‑up questions about fitness, diet, or improving your plan.")
        chat = gr.ChatInterface(fn=chatbot)

demo.launch()
