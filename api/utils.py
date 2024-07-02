import requests
from django.conf import settings


def get_client_ip(request):
    ip = request.META.get("HTTP_X_FORWARDED_FOR")
    if ip:
        ip = ip.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def get_weather_data(lat, lon):
    data = {"success": False}

    endpoint = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}&units=metric"
    response_data = requests.get(
        endpoint.format(
            lat=lat,
            lon=lon,
            key=settings.WEATHER_API_KEY,
        )
    )

    if response_data.status_code == 200:
        json_data = response_data.json()
        data["temperature"] = json_data["main"]["temp"]
        data["name"] = json_data["name"]
        data["success"] = True
    return data
