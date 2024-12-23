import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from flask import Flask, render_template, request, make_response

load_dotenv()

app = Flask(__name__)
# ---------------------------------------------------------------------------------------------------------------
def get_current_weather(city):
    api_key = os.getenv("API_KEY")
    request_url = f'https://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={city}&units=metric'  # Use metric for Celsius
    
    try:
        response = requests.get(request_url, timeout=5)  # Set a timeout for the request
        response.raise_for_status()  # Raise an error for bad responses
        weather_data = response.json()
        return weather_data
    except (requests.ConnectionError, requests.Timeout):
        return "no_connection"  # Return a specific string for no connection
    except requests.exceptions.RequestException:
        return None  # Handle other potential exceptions
# ---------------------------------------------------------------------------------------------------------------
def save_search_history(city, weather_info):
    # le dictionnaire ci dessous contient les cles et valeurs pour l'historique des recherches 
    history_entry = {
        "city": city,
        "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": weather_info["main"]["temp"],  # Celsius
        "humidity": weather_info["main"]["humidity"],  # Humidity percentage
        "wind_speed": weather_info["wind"]["speed"],  # Wind speed in meters per second
        "description": weather_info["weather"][0]["description"]
    }

    try:
        with open('search_history.json', 'r') as file:
            history = json.load(file)
    except FileNotFoundError:
        history = []

    history.append(history_entry)
    with open('search_history.json', 'w') as file:
        json.dump(history, file, indent=4)
# ---------------------------------------------------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def home():
    weather_info = None
    error_message = None
    
    if request.method == 'POST':
        city = request.form.get('city')
        weather_info = get_current_weather(city)
        
        if weather_info == "no_connection":
            error_message = "Erreur : Aucune connexion Internet ou ville non trouvée. Veuillez vérifier et réessayer."
        elif weather_info is None or weather_info.get("cod") != 200:
            error_message = "Ville non trouvée, veuillez réessayer SVP."
            weather_info = None
        else:
            save_search_history(city, weather_info)
    
    return render_template('index.html', weather_info=weather_info, error_message=error_message)
# ---------------------------------------------------------------------------------------------------------------
@app.route('/history')
def history():
    try:
        with open('search_history.json', 'r') as file:
            history = json.load(file)
    except FileNotFoundError:
        history = []

    # trier l'historique par date et temps (le plus resent affiche en premier)
    history.sort(key=lambda x: x['date_time'], reverse=True)

    return render_template('history.html', history=history)
# ---------------------------------------------------------------------------------------------------------------

@app.route('/download_csv')
def download_csv():
    try:
        with open('search_history.json', 'r') as file:
            history = json.load(file)
    except FileNotFoundError:
        history = []

    # Create the CSV response
    csv_output = "Ville,Température (°C),Humidité (%),Vitesse du Vent (km/h),Description,Date et Heure\n"
    for entry in history:
        wind_speed_kmh = entry['wind_speed'] * 3.6  # Convertir de m/s de km/h
        csv_output += f"{entry['city']},{entry['temperature']},{entry['humidity']},{wind_speed_kmh:.2f},{entry['description']},{entry['date_time']}\n"

    response = make_response(csv_output)
    response.headers["Content-Disposition"] = "attachment; filename=search_history.csv"
    response.headers["Content-Type"] = "text/csv"
    return response
# ---------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)