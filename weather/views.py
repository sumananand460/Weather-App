from django.shortcuts import render

from .forms import CityForm
from .services import get_current_weather, weather_description


def index(request):
    form = CityForm(request.GET or None)
    weather = None
    error = None

    if form.is_valid():
        city = form.cleaned_data['city']
        try:
            weather = get_current_weather(city)
            if weather is None:
                error = f'No weather data found for "{city}".'
            else:
                weather.description = weather_description(weather.weathercode)
        except Exception:
            error = 'Unable to fetch weather right now. Please try again.'

    return render(request, 'weather/index.html', {
        'form': form,
        'weather': weather,
        'error': error,
    })
