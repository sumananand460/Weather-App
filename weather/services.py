from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


GEOCODE_URL = 'https://geocoding-api.open-meteo.com/v1/search'
FORECAST_URL = 'https://api.open-meteo.com/v1/forecast'


@dataclass
class WeatherResult:
    city: str
    country: str | None
    latitude: float
    longitude: float
    temperature: float
    windspeed: float
    weathercode: int
    time: str
    timezone: str


WEATHER_CODES = {
    0: 'Clear sky',
    1: 'Mainly clear',
    2: 'Partly cloudy',
    3: 'Overcast',
    45: 'Fog',
    48: 'Depositing rime fog',
    51: 'Light drizzle',
    53: 'Moderate drizzle',
    55: 'Dense drizzle',
    56: 'Light freezing drizzle',
    57: 'Dense freezing drizzle',
    61: 'Slight rain',
    63: 'Moderate rain',
    65: 'Heavy rain',
    66: 'Light freezing rain',
    67: 'Heavy freezing rain',
    71: 'Slight snow fall',
    73: 'Moderate snow fall',
    75: 'Heavy snow fall',
    77: 'Snow grains',
    80: 'Slight rain showers',
    81: 'Moderate rain showers',
    82: 'Violent rain showers',
    85: 'Slight snow showers',
    86: 'Heavy snow showers',
    95: 'Thunderstorm',
    96: 'Thunderstorm with slight hail',
    99: 'Thunderstorm with heavy hail',
}


def geocode_city(city: str) -> dict[str, Any] | None:
    response = requests.get(
        GEOCODE_URL,
        params={'name': city, 'count': 1, 'language': 'en', 'format': 'json'},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    results = data.get('results') or []
    if not results:
        return None
    return results[0]


def get_current_weather(city: str) -> WeatherResult | None:
    location = geocode_city(city)
    if not location:
        return None

    latitude = location['latitude']
    longitude = location['longitude']
    response = requests.get(
        FORECAST_URL,
        params={
            'latitude': latitude,
            'longitude': longitude,
            'current_weather': 'true',
            'timezone': 'auto',
        },
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    current = data.get('current_weather')
    if not current:
        return None

    return WeatherResult(
        city=location.get('name', city),
        country=location.get('country'),
        latitude=latitude,
        longitude=longitude,
        temperature=current['temperature'],
        windspeed=current['windspeed'],
        weathercode=current['weathercode'],
        time=current['time'],
        timezone=data.get('timezone', 'UTC'),
    )


def weather_description(code: int) -> str:
    return WEATHER_CODES.get(code, 'Unknown weather')
