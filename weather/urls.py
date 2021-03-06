from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('init-city', views.InitCityView.as_view(), name="init_city"),
    path('city-info', views.RecordWeatherView.as_view(), name="city_info")
]
