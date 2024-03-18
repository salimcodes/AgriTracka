from flask import Flask, render_template, request
import pandas as pd
from joblib import load
import openai
import re
import requests
import sys
import os
import markdown2
from dotenv import load_dotenv

# Create a Flask web application
#app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')


# Load the pre-trained machine learning model from the joblib file
model = load('plant_growth_model.joblib')




# Load environment variables from .env file
load_dotenv()

# Configure OpenAI API
openai.api_type = os.getenv("openai.api_type")
openai.api_version = os.getenv("openai.api_version")
API_KEY = os.getenv("API_KEY")
assert API_KEY, "ERROR: Azure OpenAI Key is missing"
openai.api_key = API_KEY

RESOURCE_ENDPOINT = os.getenv("RESOURCE_ENDPOINT")
assert RESOURCE_ENDPOINT, "ERROR: Azure OpenAI Endpoint is missing"
assert "openai.azure.com" in RESOURCE_ENDPOINT.lower(), "ERROR: Azure OpenAI Endpoint should be in the form: \n\n\t<your unique endpoint identifier>.openai.azure.com"
openai.api_base = RESOURCE_ENDPOINT


def remove_markdown(text):
    # Remove Markdown headings and insert newline after each heading
    text = re.sub(r'^(#+.*)$', r'\1\n\n', text, flags=re.MULTILINE)
    # Remove Markdown syntax
    text = re.sub(r'[*_`~]', '', text)
    # Remove Markdown links
    text = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', text)
    # Remove Markdown images
    text = re.sub(r'\!\[([^]]+)\]\([^)]+\)', r'\1', text)
    return text


def remove_markdown(text):
    # Remove Markdown headings and insert two newlines after each heading
    text = re.sub(r'^(#+.*)$', r'\1\n\n', text, flags=re.MULTILINE)
    # Remove Markdown syntax
    text = re.sub(r'[*_`~]', '', text)
    # Remove Markdown links
    text = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', text)
    # Remove Markdown images
    text = re.sub(r'\!\[([^]]+)\]\([^)]+\)', r'\1', text)
    return text


# Define a route for the index page (home page)
@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize the predicted_status variable to None
    predicted_status = None

    # Check if the form is submitted using the POST method
    if request.method == 'POST':
        # Retrieve user input from the form
        light_intensity = float(request.form['light_intensity'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])

        # Create a DataFrame with the user input
        user_input = pd.DataFrame({
            'Light Intensity': [light_intensity],
            'Temperature': [temperature],
            'Humidity': [humidity]
        })

        # Use the pre-trained model to make predictions
        predicted_status = model.predict(user_input)

    # Render the index.html template and pass the predicted_status variable to the template
    return render_template('index.html', predicted_status=predicted_status)

# Define a route for the results page
@app.route('/results', methods=['GET', 'POST'])
def results():
    # Check if the form is submitted using the POST method
    if request.method == 'POST':
        # Retrieve user input from the form
        light_intensity = float(request.form['light_intensity'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])

        # Create a DataFrame with the user input
        user_input = pd.DataFrame({
            'Light Intensity': [light_intensity],
            'Temperature': [temperature],
            'Humidity': [humidity]
        })

        # Use the pre-trained model to make predictions
        predicted_status = model.predict(user_input)
        predicted_status = predicted_status[0]
         # Recommendation variable
        # Set up OpenAI Chat API
        CHAT_COMPLETIONS_MODEL = 'helping-farmers'
        ourNote = predicted_status
        prompt = """I will input the state of a farmer's plant in Lagos. I want you to return a very comprehensive recommendation on what the farmer should do to the plant mainly in terms of light intensity, temperature and humidity of the plant".
        Q: """ + ourNote + """
        A:"""
        response = openai.ChatCompletion.create(
        engine="helping-farmers",
        messages = [{"role":"system", "content":"You are a helpful assistant."},
                    {"role":"user","content":prompt},])

        recommendation = response['choices'][0]['message']['content']
        recommendation = remove_markdown(recommendation)
        
        # recommendation = "I recommend you see an agricultural expert. I recommend you see an agricultural expert.I recommend you see an agricultural expert.I recommend you see an agricultural expert." 
        #Note to Kamal; I will still change the output of the recommendation variable to something from OpenAI's model

        # Render the results.html template and pass the predicted_status variable to the template
        return render_template('results.html', predicted_status=predicted_status, recommendation=recommendation)

    # If the form is not submitted, render the results.html template with no prediction available
    return render_template('results.html', predicted_status=None)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
