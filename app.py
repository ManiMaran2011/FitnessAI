import random
import streamlit as st
from openai import OpenAI

# ---------------- CONFIGURATION ----------------
st.set_page_config(page_title="FitnessAI", page_icon="🏋️‍♂️")
st.title("🏋️‍♂️ FitnessAI — Your Personal Fitness Coach")

# ---------------- OPENAI CLIENT ----------------
api_key = st.text_input("Enter your OpenAI API key:", type="password")
client = None
if api_key and api_key.strip() != "":
    client = OpenAI(api_key=api_key)

# ---------------- MEAL & WORKOUT DATABASES ----------------
meals = [
    {"Meal": "Oatmeal with Banana", "Calories": 350},
    {"Meal": "Chicken Breast with Brown Rice", "Calories": 600},
    {"Meal": "Greek Yogurt with Berries", "Calories": 200},
    {"Meal": "Protein Shake", "Calories": 250},
    {"Meal": "Egg Omelette with Toast", "Calories": 400},
    {"Meal": "Peanut Butter Sandwich", "Calories": 350},
    {"Meal": "Grilled Fish with Veggies", "Calories": 450},
    {"Meal": "Paneer Stir Fry", "Calories": 500},
    {"Meal": "Avocado Toast", "Calories": 300},
    {"Meal": "Quinoa Salad", "Calories": 350},
    {"Meal": "Cottage Cheese Bowl", "Calories": 300},
    {"Meal": "Tuna Wrap", "Calories": 400},
    {"Meal": "Vegetable Pulao", "Calories": 450},
    {"Meal": "Smoothie Bowl", "Calories": 300},
    {"Meal": "Turkey Sandwich", "Calories": 400},
    {"Meal": "Lentil Soup with Bread", "Calories": 350},
    {"Meal": "Chickpea Curry with Rice", "Calories": 500},
    {"Meal": "Beef Stir Fry", "Calories": 550},
    {"Meal": "Fruit & Nut Mix", "Calories": 250},
    {"Meal": "Protein Pancakes", "Calories": 400},
]

workouts = [
    {"Workout Name": "Push Ups", "Category": "Bodyweight", "Reps": "15 reps"},
    {"Workout Name": "Squats", "Category": "Bodyweight", "Reps": "20 reps"},
    {"Workout Name": "Lunges", "Category": "Bodyweight", "Reps": "10 reps each leg"},
    {"Workout Name": "Plank", "Category": "Core", "Reps": "60 seconds"},
    {"Workout Name": "Burpees", "Category": "Cardio", "Reps": "10 reps"},
    {"Workout Name": "Mountain Climbers", "Category": "Cardio", "Reps": "20 reps"},
    {"Workout Name": "Bicep Curls", "Category": "Weight Training", "Reps": "12 reps"},
    {"Workout Name": "Tricep Dips", "Category": "Weight Training", "Reps": "15 reps"},
    {"Workout Name": "Overhead Press", "Category": "Weight Training", "Reps": "12 reps"},
    {"Workout Name": "Hammer Curls", "Category": "Weight Training", "Reps": "12 reps"},
    {"Workout Name": "Calf Raises", "Category": "Weight Training", "Reps": "20 reps"},
    {"Workout Name": "Dumbbell Fly", "Category": "Weight Training", "Reps": "12 reps"},
    {"Workout Name": "Leg Press", "Category": "Weight Training", "Reps": "12 reps"},
    {"Workout Name": "Barbell Row", "Category": "Weight Training", "Reps": "12 reps"},
    {"Workout Name": "Crunches", "Category": "Core", "Reps": "20 reps"},
    {"Workout Name": "Side Plank", "Category": "Core", "Reps": "30 seconds each side"},
    {"Workout Name": "Pull Ups", "Category": "Bodyweight", "Reps": "8 reps"},
    {"Workout Name": "Jumping Jacks", "Category": "Cardio", "Reps": "30 reps"},
    {"Workout Name": "Bench Press", "Category": "Weight Training", "Reps": "10 reps"},
    {"Workout Name": "Deadlift", "Category": "Weight Training", "Reps": "8 reps"},
]

# ---------------- HELPER FUNCTIONS ----------------
def calculate_target_calories(daily_calories, goal):
    if goal == "Weight Gain":
        return daily_calories + 300
    elif goal == "Weight Loss":
        return daily_calories - 300
    else:
        return daily_calories

def select_meals(target_calories):
    random.shuffle(meals)
    selected, total = [], 0
    for meal in meals:
        if total + meal["Calories"] <= target_calories:
            selected.append(meal)
            total += meal["Calories"]
        if total >= target_calories - 100:
            break
    return selected, total

def select_workouts(goal):
    if goal == "Weight Loss":
        return random.sample([w for w in workouts if w["Category"] in ["Cardio", "Bodyweight"]], 6)
    elif goal == "Weight Gain":
        return random.sample([w for w in workouts if w["Category"] == "Weight Training"], 6)
    else:
        return random.sample(workouts, 6)

def explain_plan_with_ai(height, weight, goal, daily_calories, meal_plan, workout_plan):
    if not client:
        return "Enter a valid OpenAI API key to get AI explanation."
    messages = [
        {"role": "system", "content": "You are a professional AI fitness coach."},
        {"role": "user", "content": f"Explain this fitness plan in simple words:\nHeight: {height} cm\nWeight: {weight} kg\nGoal: {goal}\nDaily Calories: {daily_calories}\nMeals: {meal_plan}\nWorkouts: {workout_plan}"}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content

# ---------------- STREAMLIT UI ----------------
st.subheader("Enter Your Details:")

col1, col2 = st.columns(2)
with col1:
    height = st.number_input("Height (cm):", min_value=100, max_value=250, value=170)
    weight = st.number_input("Weight (kg):", min_value=30, max_value=200, value=70)
with col2:
    daily_calories = st.number_input("Daily Calories:", min_value=1000, max_value=5000, value=2200)
    goal = st.selectbox("Goal:", ["Weight Loss", "Weight Gain", "Maintenance"])

if st.button("Generate Plan 💪"):
    target_calories = calculate_target_calories(daily_calories, goal)
    selected_meals, total_meal_cal = select_meals(target_calories)
    workout_plan = select_workouts(goal)

    st.success("✅ Plan Generated!")

    # Meals
    st.write("### 🍽 Recommended Meals:")
    for meal in selected_meals:
        st.write(f"- {meal['Meal']} ({meal['Calories']} kcal)")
    st.write(f"**Total:** {total_meal_cal} kcal (Target: {target_calories} kcal)")

    # Workouts
    st.write("### 💪 Workout Plan:")
    for w in workout_plan:
        st.write(f"- {w['Workout Name']} | {w['Category']} | {w['Reps']}")

    # AI explanation
    meal_names = [m["Meal"] for m in selected_meals]
    workout_names = [w["Workout Name"] for w in workout_plan]
    with st.spinner("🤖 FitnessAI is explaining your plan..."):
        explanation = explain_plan_with_ai(height, weight, goal, daily_calories, meal_names, workout_names)
    st.write("### 🤖 FitnessAI says:")
    st.info(explanation)

# ---------------- CHAT ----------------
st.divider()
st.subheader("💬 Chat with FitnessAI")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hey! I'm your FitnessAI coach. Ask me anything about workouts, meals, or your plan!"}
    ]

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.markdown(f"🤖 **FitnessAI:** {msg['content']}")
    else:
        st.markdown(f"**You:** {msg['content']}")

user_input = st.text_input("Type your question:")
if st.button("Send"):
    if user_input and client:
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        ai_reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
