import requests

def get_weather(lat, lon, exclude, units, appid):
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={exclude}&units={units}&appid={appid}"
    return requests.get(url)

def get_historical_weather(lat, lon, dt, units, appid):
    url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={dt}&units={units}&appid={appid}"
    return requests.get(url)