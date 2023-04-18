import tkn
import requests
import json

apiKey = (tkn.nasaTkn)

def POD(date):
    pictureoftheday = requests.get(f"https://api.nasa.gov/planetary/apod/?date={date}&api_key={apiKey}")
    nasaPOD = json.loads(pictureoftheday.text)["url"]
    return (nasaPOD)

def satellite(lat, lon):
    satelliterequests = requests.get(f"https://api.nasa.gov/planetary/earth/assets?lon={lon}&lat={lat}&date=2015-02-01&dim=0.1&{apiKey}")
    satelliteimg = json.loads(satelliterequests.text)["url"]
    return (satelliteimg)



