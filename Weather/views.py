from django.views.generic import TemplateView
from django.shortcuts import render
from .models import Info, City
from django.http import JsonResponse
from django.utils import timezone
from . import applogic
from django.core.exceptions import ObjectDoesNotExist
import xml.etree.ElementTree as ET


class IndexView(TemplateView):
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        context = {}
        try:
            data = ET.fromstring(applogic.get_current_weather(request.POST['lat'], request.POST['lon']).content)
            context['Temp_max'] = '{:+.0f} °C'.format(float(data[1].attrib['min']))
            context['Wind'] = '{}, {} m/s, {} ({:.0f})'.format(data[4][0].attrib['name'], data[4][0].attrib['value'],
                                                           data[4][2].attrib['name'], float(data[4][2].attrib['value']))
            context['Pressure'] = '{:.0f} hpa'.format(float(data[3].attrib['value']))
            context['Humidity'] = '{} %'.format(data[2].attrib['value'])
            context['Cloudiness'] = data[8].attrib['value']
            context['Sunrise'] = '%s UTC' % timezone.datetime.strptime(data[0][2].attrib['rise'],
                                                                       "%Y-%m-%dT%X").strftime("%H:%M")
            context['Sunset'] = '%s UTC' % timezone.datetime.strptime(data[0][2].attrib['set'],
                                                                      "%Y-%m-%dT%X").strftime("%H:%M")
            context['Country'] = data[0][1].text
            context['Name'] = data[0].attrib['name']
            context['Temp'] = '{:+.0f}'.format(float(data[1].attrib['value']))
            context['WeatherIcon'] = data[8].attrib['icon']
            context['Country_icon_low'] = str(data[0][1].text).lower()
            return JsonResponse(context)
        except Exception as e:
            print("Exception (find):", e)

        try:
            data = applogic.find_city(request.POST['term'])

            for city in data['list']:
                context[city['id']] = '{}, {}'.format(city['name'], city['sys']['country'])
            return JsonResponse(context)
        except Exception as e:
            print("Exception (find):", e)

        return render(request, self.template_name)


class ForecastView(TemplateView):
    template_name = "forecast.html"

    def post(self, request, *args, **kwargs):
        context = {}
        try:
            data = applogic.find_city(request.POST['term'])

            for city in data['list']:
                context[city['id']] = '{}, {}'.format(city['name'], city['sys']['country'])
            return JsonResponse(context)
        except Exception as e:
            print("Exception (find):", e)

        return render(request, self.template_name)

    def get_context_data(self, **kwargs):
        context = super(ForecastView, self).get_context_data(**kwargs)
        city_id = self.kwargs.get('id')

        try:
            obj = City.objects.get(id=city_id)
            Info.objects.filter(city=obj).filter(date__lte=timezone.now()).delete()
            city_weather = Info.objects.filter(city=obj)

            if city_weather.__len__() <= 32:
                applogic.update_forecast(city_id)
                city_weather = Info.objects.filter(city=obj)

            context['city_info'] = obj
            context['forecast_db'] = city_weather
        except ObjectDoesNotExist:
            print("City with id:{} wasn't found in database.".format(city_id))
            data = applogic.get_forecast(self.kwargs.get('id'))
            context['forecast_list'] = data

        return context
