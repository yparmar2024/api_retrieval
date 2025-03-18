import requests

"""
LOCATION DOCUMENTATION: 
https://ipinfo.io/developers

WEATHER DOCUMENTATION:
https://openweathermap.org/api/one-call-3
"""

city = ""
locationAPI = "f04808a639eac9"
weatherAPI = "a886740285ce090a299adf2ef217fd05"

def start():
    getLocation()
    getWeather()

def getLocation():
    global city
    global locationAPI

    url = f"https://ipinfo.io?token={locationAPI}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        city = data.get('city')
        return city
    else:
        city = None
        return f"Error: Unable to fetch data for your IP address"
    
def getWeather():
    global city
    global weatherAPI

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weatherAPI}&units=imperial"
    response = requests.get(url)

    if city != None:
        if response.status_code == 200:
            data = response.json()
            print(f"The current weather in {city} is {data["weather"][0]["description"]} with a temperature of {data["main"]["temp"]} degrees Fahrenheit which feels like {data["main"]["feels_like"]} degrees with a wind speed of {data["wind"]["speed"]} miles per hour.")
        else:
            return f"Error: Unable to fetch a weather for your city"
    else:
        return f"Error: Unable to fetch data for your IP address"