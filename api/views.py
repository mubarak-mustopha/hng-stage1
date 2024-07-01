from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.gis.geoip2 import GeoIP2
from django.conf import settings


import requests


# Create your views here.
# https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key} --> https://openweathermap.org/current
# http://api.openweathermap.org/geo/1.0/reverse?lat=51.5098&lon=-0.1180&limit=5&appid={API key} --> https://openweathermap.org/api/geocoding-api
# https://api.openweathermap.org/data/2.5/weather?lat=57&lon=-2.15&appid={API key}&units=metric --> https://openweathermap.org/current#data
# key --> b62040e2dcd50d3763d87680c4bcb714
# https://docs.djangoproject.com/en/5.0/ref/contrib/gis/geoip2/


@require_http_methods(["GET"])
def home(request):
    name = request.GET.get("name", "Anonymous")

    response = {}

    # client ip
    client_ip = request.META.get("HTTP_X_FORWARDED_FOR")
    if client_ip:
        client_ip = client_ip.split(",")[0]
    else:
        client_ip = request.META.get("REMOTE_ADDR")
    response["client_ip"] = client_ip

    # weather data
    ip = "google.com"
    g = GeoIP2().city(ip)
    print(g)
    location = g["city"]
    lat = g["latitude"]
    lon = g["longitude"]

    weather_data_endpoint = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}&units=metric"
    weather_response_data = requests.get(
        weather_data_endpoint.format(
            lat=lat,
            lon=lon,
            key=settings.WEATHER_API_KEY,
        )
    )

    weather_json_data = weather_response_data.json()

    if weather_response_data.status_code == 200:
        temperature = weather_json_data["main"]["temp"]
        if not location:
            location = weather_json_data["name"]
        response["location"] = location
        response["greeting"] = (
            f"Hello {name}!, the temperature is {temperature} degrees Celcius in {location}"
        )
    else:
        response["greeting"] = (
            f"Hello {name}!, sorry we could not get weather information for {location}"
        )

    return JsonResponse(response)
