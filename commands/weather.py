import requests
from telethon import TelegramClient, events
from translations import translations
import os

API_KEY = '# Insert the key of openweathermap.org here'

async def get_weather(city_name):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city_name}&appid={API_KEY}&units=metric"
    response = requests.get(complete_url)

    if response.status_code == 200:
        data = response.json()
        main = data['main']
        wind = data['wind']
        weather_desc = data['weather'][0]['description']
        city = data['name']
        country = data['sys']['country']

        temperature = main['temp']
        pressure = main['pressure']
        humidity = main['humidity']
        wind_speed = wind['speed']

        weather_info = (
            f"{translations['weather_in']} {city}, {country}:\n\n"
            f"{translations['temperature']}: {temperature}°C\n"
            f"{translations['humidity']}: {humidity}%\n"
            f"{translations['wind_speed']}: {wind_speed} m/s\n"
            f"{translations['description']}: {weather_desc.capitalize()}\n"
            f"{translations['pressure']}: {pressure} hPa"
        )
        return weather_info
    else:
        return translations['city_not_found']

async def weather_command(event):
    message = event.raw_text
    city_name = message.split('.wt', maxsplit=1)[1].strip()

    if not city_name:
        await event.edit(translations['ask_city'])
        return

    weather_info = await get_weather(city_name)
    await event.edit(weather_info)

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.wt .+', outgoing=True))
    async def handler(event):
        await weather_command(event)
