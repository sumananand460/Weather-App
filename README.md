# Django Weather App

A simple Django weather app that lets users search for a city and see the current weather.

## Features
- City search form
- Current temperature and wind speed
- Weather description
- Responsive UI
- No API key required (uses Open-Meteo)

## Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Notes
- The app uses Open-Meteo geocoding and weather APIs.
- Internet access is required when searching for weather.

- By Suman Anand