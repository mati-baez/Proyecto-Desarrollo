
import requests

GEO_BASE = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_BASE = "https://api.open-meteo.com/v1/forecast"

def buscar_coords(ciudad: str):
    r = requests.get(GEO_BASE, params={"name": ciudad, "count": 1, "language": "es", "format": "json"}, timeout=12)
    r.raise_for_status()
    data = r.json()
    if not data.get("results"):
        return None, None
    first = data["results"][0]
    return first["latitude"], first["longitude"]

def clima_actual(lat: float, lon: float):
    r = requests.get(FORECAST_BASE, params={"latitude": lat, "longitude": lon, "current_weather": "true"}, timeout=12)
    r.raise_for_status()
    return (r.json() or {}).get("current_weather", {})
