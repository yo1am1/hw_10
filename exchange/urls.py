from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("exch/", views.add_param, name="calculate"),
    path("vkurse/", views.vkurse, name="vkurse"),
    path("currencyapi/", views.currencyapi, name="currencyapi"),
    path("nbu/", views.nbu, name="nbu"),
]
