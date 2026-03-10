from flask import Flask, render_template, request
import pandas as pd
from joblib import load
import openai
import re
import os
from dotenv import load_dotenv


# -----------------------------
# Flask App Setup
# -----------------------------

app = Flask(__name__, static_url_path='/static')


# -----------------------------
# Load ML Model
# -----------------------------

model = load('plant_growth_model.joblib')


# -----------------------------
# Load Environment Variables
# -----------------------------

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing from .env file")

openai.api_key = OPENAI_API_KEY


# -----------------------------
# Utility Function
# -----------------------------

def remove_markdown(text):
    text = re.sub(r'^(#+.*)$', r'\1\n\n', text, flags=re.MULTILINE)
    text = re.sub(r'[*_`~]', '', text)
    text = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'\!\[([^]]+)\]\([^)]+\)', r'\1', text)
    return text


# -----------------------------
# Home Page
# -----------------------------

@app.route('/', methods=['GET', 'POST'])
def index():

    predicted_status = None

    if request.method == 'POST':

        light_intensity = float(request.form['light_intensity'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])

        user_input = pd.DataFrame({
            'Light Intensity': [light_intensity],
            'Temperature': [temperature],
            'Humidity': [humidity]
        })

        predicted_status = model.predict(user_input)

    return render_template('index.html', predicted_status=predicted_status)


# -----------------------------
# Results Page
# -----------------------------

@app.route('/results', methods=['GET', 'POST'])
def results():

    if request.method == 'POST':

        light_intensity = float(request.form['light_intensity'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])

        user_input = pd.DataFrame({
            'Light Intensity': [light_intensity],
            'Temperature': [temperature],
            'Humidity': [humidity]
        })

        predicted_status = model.predict(user_input)[0]

        # -----------------------------
        # Prompt for AI Recommendation
        # -----------------------------

        prompt = f"""
        A farmer in Lagos has a plant with the following predicted condition: {predicted_status}.

        Provide a clear and practical recommendation for the farmer to improve the plant's health.

        Focus specifically on adjustments to:
        - light intensity
        - temperature
        - humidity

        Explain the reasoning behind each recommendation.
        """

        # -----------------------------
        # OpenAI API Call
        # -----------------------------

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an agricultural expert helping farmers optimize plant growth."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        recommendation = response['choices'][0]['message']['content']
        recommendation = remove_markdown(recommendation)

        return render_template(
            'results.html',
            predicted_status=predicted_status,
            recommendation=recommendation
        )

    return render_template('results.html', predicted_status=None)


# -----------------------------
# Run Server
# -----------------------------

if __name__ == '__main__':
    app.run(debug=True)