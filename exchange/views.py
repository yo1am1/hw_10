import datetime
import decimal

import currencyapicom
import requests
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import RateForm
from .models import Rate


class DecimalAsFloatJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super().default(o)


def index(request):
    current_date = datetime.date.today()
    current_rates = Rate.objects.filter(date=current_date).all().values()
    return JsonResponse(
        {"current_rates": list(current_rates)}, encoder=DecimalAsFloatJSONEncoder
    )


def add_param(request):
    if request.method == "POST":
        form = RateForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("add_param"))
        else:
            form = RateForm()
        context = {"form": form}
        return render(request, "exchange_form.html", context)


def vkurse(request):
    r = requests.get("https://vkurse.dp.ua/course.json")
    answer = r.json()

    return JsonResponse(answer, encoder=DecimalAsFloatJSONEncoder)


def currencyapi(request):
    client = currencyapicom.Client("YQeLH52G55DlV361wbi6Vs1cDj3Jg0TG2KTSBIG6")
    result = client.latest()

    return JsonResponse(result, encoder=DecimalAsFloatJSONEncoder)


def nbu(request):
    r = requests.get(
        "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    )
    answer = r.json()

    return JsonResponse(answer, encoder=DecimalAsFloatJSONEncoder, safe=False)
