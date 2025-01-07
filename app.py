from flask import Flask, render_template, request
import requests
import geoip2


app = Flask(__name__)

# Replace with your OpenWeatherMap API key
API_KEY = '562b40d8ff660d9da660fdffcce5812f'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

@app.route('/')
def index():
    # Use a geolocation API to detect user's city
    ip_api_url = 'http://ip-api.com/json'
    response = requests.get(ip_api_url)
    city = None
    if response.status_code == 200:
        location_data = response.json()
        city = location_data.get('city', 'Nairobi')  # Default to Nairobi
    return render_template('index.html', city=city)

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form.get('city')
    api_key = '562b40d8ff660d9da660fdffcce5812f'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        condition = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        
        # Determine the background based on the condition
        condition_lower = condition.lower()
        if 'rain' in condition_lower:
            background_url = 'https://res.cloudinary.com/dtgnjlnnm/image/upload/v1736269387/rain-3518956_wtbwln.jpg'
        elif 'cloud' in condition_lower:
            background_url = 'https://res.cloudinary.com/dtgnjlnnm/image/upload/v1736269386/darling-7838296_m7dc0u.jpg'
        elif 'snow' in condition_lower:
            background_url = 'https://res.cloudinary.com/dtgnjlnnm/image/upload/v1736269529/snow-7646952_a453yr.jpg'
        elif 'clear' in condition_lower:
            background_url = 'https://res.cloudinary.com/dtgnjlnnm/image/upload/v1736269403/sun-3588618_xa5q9e.jpg'
        else:
            background_url = 'https://res.cloudinary.com/dtgnjlnnm/image/upload/v1736269443/meadow-95724_qgc3r8.jpg'
        
        return render_template(
            'weather.html',
            city=city,
            temperature=temperature,
            feels_like=feels_like,
            condition=condition,
            humidity=humidity,
            wind_speed=wind_speed,
            background_url=background_url
        )
    else:
        return "City not found", 404

@app.route('/forecast/<city>')
def forecast(city):
    api_key = '562b40d8ff660d9da660fdffcce5812f'
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast_data = []
        
        # Extract forecast for every 3 hours
        for item in data['list']:
            forecast_data.append({
                'date': item['dt_txt'],
                'temp': item['main']['temp'],
                'condition': item['weather'][0]['description'],
            })
        
        return render_template('forecast.html', city=city, forecast_data=forecast_data)
    else:
        return "Forecast data not found", 404

if __name__ == '__main__':
    app.run(debug=True)
