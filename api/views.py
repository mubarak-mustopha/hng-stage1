from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.gis.geoip2 import GeoIP2


from .utils import get_weather_data, get_client_ip


@require_http_methods(["GET"])
def home(request):
    name = request.GET.get("visitor_name", "Anonymous")

    response = {}

    # client ip address
    client_ip = get_client_ip(request)
    response["client_ip"] = client_ip

    # geoip
    g = GeoIP2().city(client_ip)
    weather_data = get_weather_data(g["latitude"], g["longitude"])

    if not weather_data["success"]:
        response["location"] = g["city"]
        response["greeting"] = (
            f"Hello {name}!, sorry we could not get weather information for {g['city']}"
        )

    else:
        response["location"] = g["city"] or weather_data["name"]
        temperature = weather_data["temperature"]
        response["greeting"] = (
            f"Hello {name}!, the temperature is {temperature} degrees Celcius in {response['location']}"
        )

    return JsonResponse(response)
