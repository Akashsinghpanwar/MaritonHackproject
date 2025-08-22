from __future__ import annotations
import os, requests
from typing import Any, Dict

OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY") or os.getenv("WEATHER_API_KEY")

def forecast_latlon(lat: float, lon: float) -> Dict[str, Any]:
    """Simple OpenWeather OneCall wrapper (requires key)."""
    if not OPENWEATHER_KEY:
        return {"error": "WEATHER_API_KEY/OPENWEATHER_KEY not set."}
    url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {"lat": lat, "lon": lon, "appid": OPENWEATHER_KEY, "units": "metric"}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json()
