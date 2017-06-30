import requests
from Weather.models import City, Info
import warnings
from django.utils import timezone
import pytz

app_id = "22a9252e0c35943130925da146e5706f"

warnings.filterwarnings(
        'ignore', r"DateTimeField .* received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')


def get_current_weather(latitude, longitude):
    res = {}
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'lat': latitude, 'lon': longitude, 'units': 'metric',
                                   'mode': 'xml', 'APPID': app_id})

    except Exception as e:
        print("Exception (find in get_current_weather):", e)

    return res


def find_city(city_name):
    cities = {}
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': city_name, 'type': 'like', 'units': 'metric', 'APPID': app_id})
        cities = res.json()

        cities['find_city'] = city_name
        for city in cities['list']:
            city['main']['temp'] = '{:+.0f}'.format(city['main']['temp'])
            city['sys']['country_low'] = city['sys']['country'].lower()
    except Exception as e:
        print("Exception (find in find_city):", e)

    return cities


def update_forecast(city_id):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'APPID': app_id})
        data = res.json()
        city_model = City.objects.get(id=city_id)
        date_last = Info.objects.filter(city=city_model).latest('date').date

        for forecast in data['list']:
            if date_last <= timezone.datetime.fromtimestamp(int(forecast['dt']), tz=pytz.UTC):
                model = Info(
                    city=city_model,
                    date=str(timezone.datetime.fromtimestamp(forecast['dt'])),
                    temperature=forecast['main']['temp'],
                    pressure=forecast['main']['pressure'],
                    humidity=forecast['main']['humidity'],
                    wind_speed=forecast['wind']['speed'],
                    weather_description=forecast['weather'][0]['description']
                )
                model.save()
    except Exception as e:
        print("Exception (find in update_forecast):", e)


def get_forecast(city_id):
    data = {}
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'APPID': app_id})
        data = res.json()
        city_model = City(
            id=data['city']['id'],
            name=data['city']['name'],
            country=data['city']['country'],
            coord_longitude=data['city']['coord']['lon'],
            coord_latitude=data['city']['coord']['lat']
        )
        city_model.save()
        for forecast in data['list']:
            forecast['dt'] = str(timezone.datetime.fromtimestamp(forecast['dt']))
            forecast['main']['temp'] = '{:+.0f}'.format(float(forecast['main']['temp']))
            forecast['main']['pressure'] = '{:.0f}'.format(float(forecast['main']['pressure']))
            model = Info(
                    city=city_model,
                    date=forecast['dt'],
                    temperature=forecast['main']['temp'],
                    pressure=forecast['main']['pressure'],
                    humidity=forecast['main']['humidity'],
                    wind_speed=forecast['wind']['speed'],
                    weather_description=forecast['weather'][0]['description']
            )
            model.save()
    except Exception as e:
        print("Exception (find in get_forecast):", e)

    return data
