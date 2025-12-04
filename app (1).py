
import os
import sys
import argparse
from typing import Dict, Any

try:
    from openai import OpenAI
except Exception as e:
    print("Failed to import openai. Did you install requirements? pip install -r requirements.txt")
    raise

# --- Config & client ---
def get_client() -> Any:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY is not set. Set it in your environment or .env file.")
        sys.exit(1)
    try:
        client = OpenAI(api_key=api_key)
        return client
    except Exception as e:
        print(f"Failed to initialize OpenAI client: {e}")
        sys.exit(1)

# --- Core generators ---
def generate_plan(client, profile: Dict[str, Any]) -> Dict[str, str]:
    """Generate workout and meal plans using the LLM."""
    system = "You are a certified fitness and nutrition coach. Be specific, safe, and actionable."
    user = f"""Create a personalized plan.
    Profile:
    - Height: {profile['height_cm']} cm
    - Weight: {profile['weight_kg']} kg
    - Age: {profile['age']}
    - Sex: {profile['sex']}
    - Goal: {profile['goal']} (e.g., fat loss, muscle gain, maintenance)
    - Experience: {profile['experience']} (beginner/intermediate/advanced)
    - Diet: {profile['diet']} (e.g., veg, non-veg, vegan, etc.)
    - Constraints: {profile['constraints']}

    Return two sections with markdown headings:
    ### Workout Plan
    - 7-day schedule with sets/reps, progression tips, and rest days.
    - Include warm-up and cooldown guidance.

    ### Meal Plan
    - 7-day menu with sample meals, portion guidance, and macros approx.
    - Provide 2 snack suggestions per day.
    - Account for the diet preference and constraints.
    """
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.4,
        messages=[
            {"role":"system","content":system},
            {"role":"user","content":user}
        ],
    )
    content = completion.choices[0].message.content
    # Split by sections if needed; for simplicity return the whole content for both
    return {"workout": content, "meals": content}

def chat_loop(client, context: str):
    """Simple interactive chatbot. Type 'exit' to quit."""
    print("\n--- Chatbot started (type 'exit' to quit) ---")
    history = [
        {"role":"system","content":"You are a helpful fitness and nutrition assistant."},
        {"role":"user","content": f"Context to keep in mind: {context}"}
    ]
    while True:
        user = input("\nYou: ").strip()
        if user.lower() in {"exit", "quit", "q"}:
            print("Chatbot ended.")
            break
        history.append({"role":"user","content":user})
        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.4,
                messages=history[-12:],  # keep recent context short
            )
            msg = resp.choices[0].message.content
            print(f"AI: {msg}")
            history.append({"role":"assistant","content":msg})
        except Exception as e:
            print(f"AI error: {e}")

def main():
    parser = argparse.ArgumentParser(description="FitnessAI - Personalized fitness & meal plans + chatbot")
    parser.add_argument("--height_cm", type=int, help="Height in cm")
    parser.add_argument("--weight_kg", type=float, help="Weight in kg")
    parser.add_argument("--age", type=int, help="Age in years")
    parser.add_argument("--sex", type=str, choices=["male","female","other"], help="Sex")
    parser.add_argument("--goal", type=str, help="Goal: fat loss, muscle gain, maintenance, etc.")
    parser.add_argument("--experience", type=str, default="beginner", help="Experience level")
    parser.add_argument("--diet", type=str, default="non-veg", help="veg / non-veg / vegan / etc.")
    parser.add_argument("--constraints", type=str, default="none", help="Injuries, allergies, equipment limits, etc.")
    parser.add_argument("--no_chat", action="store_true", help="Skip chatbot after plan generation")
    args = parser.parse_args()

    # Prompt missing inputs interactively
    def ask_if_none(val, prompt, cast=str):
        if val is not None:
            return val
        while True:
            try:
                entered = cast(input(prompt).strip())
                return entered
            except Exception:
                print("Invalid input, try again.")

    profile = {
        "height_cm": ask_if_none(args.height_cm, "Enter height (cm): ", int),
        "weight_kg": ask_if_none(args.weight_kg, "Enter weight (kg): ", float),
        "age": ask_if_none(args.age, "Enter age: ", int),
        "sex": ask_if_none(args.sex, "Enter sex (male/female/other): "),
        "goal": ask_if_none(args.goal, "Enter goal (fat loss/muscle gain/maintenance): "),
        "experience": args.experience,
        "diet": args.diet,
        "constraints": args.constraints,
    }

    client = get_client()
    plans = generate_plan(client, profile)

    print("\n===== WORKOUT & MEAL PLAN =====\n")
    print(plans["workout"])

    if not args.no_chat:
        context = (
            f"User profile: {profile}. Use the above plan as context. "
            "Answer questions, adjust recommendations, and be concise."
        )
        chat_loop(client, context)

if __name__ == "__main__":
    main()
