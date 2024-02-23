import os
import requests
from dotenv import load_dotenv


# Загружаем переменные окружения
load_dotenv()


def fetch_weather(city):
    # Получаем апи ключ из переменных окружения
    api_key = os.getenv("WEATHER_API_KEY")
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)

    # Проверяем статус запроса, если он удачный, возвращаем значение
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        return temperature
    else:
        return None
