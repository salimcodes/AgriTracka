from flask import Flask, render_template, request
import pandas as pd
from joblib import load
import openai
import re
import requests
import sys
import os
import markdown2
import time
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
        #CHAT_COMPLETIONS_MODEL = 'helping-farmers'
        #ourNote = predicted_status
        #prompt = """I will input the state of a farmer's plant in Lagos. I want you to return a very comprehensive recommendation on what the farmer should do to the plant mainly in terms of light intensity, temperature and humidity of the plant".
        #Q: """ + ourNote + """
        #A:"""
        #response = openai.ChatCompletion.create(
        #engine="helping-farmers",
        #messages = [{"role":"system", "content":"You are a helpful assistant."},
        #            {"role":"user","content":prompt},])

        #recommendation = response['choices'][0]['message']['content']
        #recommendation = remove_markdown(recommendation)
        

        if predicted_status.lower() == 'healthy':
            recommendation = "As an agriculturist, if you've predicted that a farmer's plant is healthy based on sensor data including light intensity, temperature, and humidity, it's essential to continue monitoring these factors regularly to ensure the continued health and growth of the plants. Here are some recommendations: 1. Regular Monitoring: Maintain a schedule for monitoring the environmental conditions in the farm, including light intensity, temperature, and humidity. This will help in early detection of any deviations that might affect plant health. 2. Optimize Light Conditions: Ensure that the plants receive adequate light for photosynthesis, as insufficient light can hinder growth. Consider installing artificial lighting if natural light is insufficient, especially during cloudy days or in indoor farming setups. 3. Manage Temperature: Keep the temperature within the optimal range for the specific plant species being cultivated. Sudden fluctuations or extremes in temperature can stress the plants and make them more susceptible to diseases. 4. Control Humidity Levels: Maintain optimal humidity levels to prevent issues such as mold growth or wilting. Adequate ventilation and the use of humidifiers or dehumidifiers can help regulate humidity levels as needed. 5. Nutrient Management: Ensure that the plants are receiving adequate nutrients through soil fertilization or hydroponic nutrient solutions. Regularly test the soil or nutrient solution to adjust the fertilizer application as necessary. 6. Pest and Disease Monitoring: Keep an eye out for any signs of pests or diseases, as even healthy-looking plants can be vulnerable. Implement integrated pest management strategies to control pests and diseases while minimizing environmental impact. By following these recommendations and maintaining a proactive approach to farm management based on sensor data, you can help ensure the continued health and success of the farmer's plants."
        elif predicted_status.lower() == 'struggling':
            recommendation = "If the output indicates that the plants are struggling based on the sensor data, it's crucial to take immediate action to address the underlying issues and improve plant health. Here's how you can proceed: 1. Investigate Environmental Factors: Analyze the sensor data to identify any anomalies or deviations in light intensity, temperature, or humidity that could be contributing to the plants' struggles. Determine if there are specific areas where conditions are less than optimal. 2. Adjust Light Conditions: If light intensity is inadequate, consider repositioning grow lights or increasing their intensity to ensure sufficient light for photosynthesis. Evaluate the placement of shading structures or nearby obstacles that may be blocking natural light. 3. Stabilize Temperature: If temperature fluctuations are causing stress to the plants, implement measures to stabilize temperatures within the recommended range. This may involve adjusting ventilation, insulating structures, or using climate control systems. 4. Optimize Humidity Levels: Ensure that humidity levels are within the optimal range for the plants' growth stage. Use humidifiers or dehumidifiers as needed to maintain consistent humidity levels and prevent moisture-related issues like mold or wilting. 5. Review Nutrient Availability: Assess the availability of essential nutrients in the soil or hydroponic system. Conduct soil tests or analyze nutrient solutions to determine if any deficiencies are affecting plant health. Adjust fertilizer application or nutrient solutions accordingly. By promptly addressing the factors contributing to the plants' struggles and implementing targeted interventions based on sensor data analysis, you can help improve their health and resilience, ultimately supporting the farmer's success in crop cultivation."
        elif predicted_status.lower() == 'growing':   
            recommendation = "If the sensor data indicates that the plants are in a growing state, it suggests that they are developing well under the current environmental conditions. Here's how you can continue to support their growth: 1. Maintain Optimal Conditions: Continue monitoring and maintaining ideal levels of light intensity, temperature, and humidity as indicated by the sensor data. Consistency in environmental conditions is crucial for uninterrupted growth. 2. Adjust as Needed: Regularly assess the sensor data to detect any fluctuations or deviations in environmental factors. Adjust lighting, ventilation, and other parameters as necessary to ensure that the plants remain in an optimal growing environment. 3. Nutrient Management: Monitor nutrient levels in the soil or hydroponic system and provide appropriate fertilization to support healthy growth. Adjust nutrient solutions based on the growth stage of the plants and any changes observed in sensor data. 4. Support Structural Development: Provide adequate support structures for the plants to encourage proper growth and prevent damage. This is particularly important for tall or vining plants that may require trellising or staking. 5. Monitor for Pests and Diseases: Regularly inspect the plants for signs of pests or diseases, even if they appear to be growing well. Early detection allows for prompt intervention to prevent the spread of pests or diseases and minimize damage to the plants. 6. Pruning and Training: Prune the plants as needed to remove dead or diseased foliage and promote healthy growth. Train plants to grow in desired shapes or patterns to optimize space and sunlight exposure. 7. Encourage Pollination: If growing flowering plants, encourage pollination by providing habitat for pollinators or gently shaking the plants to distribute pollen. This promotes fruit set and ensures healthy seed development. By following these recommendations and leveraging the insights provided by sensor data, you can continue to support the healthy growth and development of the plants, ultimately contributing to a successful harvest."
        elif predicted_status.lower() == 'dormant':
            recommendation = "If the sensor data indicates that the plants are in a dormant state, it suggests that they are currently inactive or resting, which is a natural phase in their growth cycle. Here's how you can manage the plants during this period: 1. Reduce Maintenance: During dormancy, plants require less attention compared to active growth periods. Reduce watering frequency but ensure that the soil remains slightly moist to prevent dehydration. 2. Monitor Environmental Conditions: While plants are dormant, continue to monitor environmental factors such as temperature and humidity to ensure they remain within acceptable ranges. Extreme fluctuations in temperature or humidity can still negatively impact dormant plants. 3. Minimize Disturbance: Avoid disturbing dormant plants unnecessarily. Minimize pruning or transplanting activities during this period to allow the plants to rest undisturbed. 4. Protect from Extreme Conditions: Provide protection from harsh weather conditions, such as frost or excessive wind, which can damage dormant plants. Consider using frost cloths or mulch to insulate the soil and protect the roots. 5. Disease Prevention: Keep an eye out for signs of disease or pest infestation, as dormant plants may still be vulnerable to certain pathogens. Take appropriate measures to prevent the spread of disease and minimize pest damage. 6. Prepare for Active Growth: Use the dormant period to prepare for the upcoming growing season. Prune dead or damaged branches, clean up debris around the plants, and apply dormant sprays or treatments as needed to prevent pests and diseases. 7. Maintain Records: Keep detailed records of environmental conditions and observations during the dormant period. This information can help you track the plants' health and growth progress over time. By following these guidelines, you can effectively manage dormant plants and set the stage for healthy growth and productivity when they awaken from their dormancy."
        elif predicted_status.lower() == 'thriving':
            recommendation = "If the sensor data indicates that the plants are thriving, it suggests that they are growing vigorously and exhibiting optimal health. Here's how you can continue to support their thriving status: 1. Ensure that the environmental parameters are consistently maintained at their peak levels: Ensure that the environmental conditions, including light intensity, temperature, and humidity, remain within the ideal ranges as indicated by the sensor data. Consistency in these factors is key to sustaining thriving growth. 2. Regular Monitoring: Continue to monitor the sensor data regularly to detect any changes or fluctuations in environmental conditions. Promptly address any deviations to prevent potential stress to the plants.3. Provide Adequate Nutrients: Supply the plants with sufficient nutrients through fertilization or nutrient solutions. Monitor nutrient levels and adjust fertilization practices based on plant growth and development stages. 4. Water Management: Maintain proper watering practices to ensure that the plants receive adequate moisture without waterlogging the soil. Adjust watering frequency based on weather conditions and plant requirements. 5. Pruning and Maintenance: Prune the plants as needed to remove dead or diseased foliage, promote airflow, and shape the plants for optimal growth. Regular maintenance tasks such as weeding and mulching should also be performed to support plant health. 6. Pest and Disease Prevention: Continue to monitor the plants for signs of pests or diseases and implement preventive measures to avoid infestations. This may include using natural predators, applying organic pesticides, or practicing good sanitation habits. 7. Record Keeping and Analysis: Maintain detailed records of plant growth, health, and environmental conditions. Analyze this data to identify trends and patterns that can inform future growing practices and optimize plant performance. By following these recommendations and leveraging the insights provided by sensor data, you can continue to nurture thriving plants and promote their ongoing health and vitality."
        #recommendation = "I recommend you see an agricultural expert. I recommend you see an agricultural expert.I recommend you see an agricultural expert.I recommend you see an agricultural expert." 
        #Note to Kamal; I will still change the output of the recommendation variable to something from OpenAI's model
        time.sleep(7)
        # Render the results.html template and pass the predicted_status variable to the template
        return render_template('results.html', predicted_status=predicted_status, recommendation=recommendation)

    # If the form is not submitted, render the results.html template with no prediction available
    return render_template('results.html', predicted_status=None)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
