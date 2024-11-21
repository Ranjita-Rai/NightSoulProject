from django.shortcuts import render
import requests
from django.conf import settings
from .models import WeatherApp  # Import your model

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    return data

def weatherApp(request):
    city = ''
    weather_data = None

    if 'city' in request.POST:
        city = request.POST['city']
        weather_data = get_weather_data(city)

        if weather_data.get('cod') == 200:
            # Save weather data to the database
            WeatherApp.objects.update_or_create(
                city=city,
                defaults={
                    'temperature': weather_data['main']['temp'],
                    'humidity': weather_data['main']['humidity'],
                    'wind_speed': weather_data['wind']['speed'],
                    'description': weather_data['weather'][0]['description'],
                }
            )
        else:
            weather_data = None  # If city not found, set data to None

    return render(request, 'weatherApp/weather.html', {'city': city, 'weather_data': weather_data})
