from django.http import HttpResponse, JsonResponse
# from django.views.generic.base import TemplateView
from django.views import View
from .task import init_city


def index(request):
    return HttpResponse("你好，这里是测试demo")


class InitCityView(View):
    """ 初始化城市字典 """
    def get(self, request):
        return HttpResponse("请调用post方法")

    def post(self, request):
        init_city.get_city_data()
        return JsonResponse({"info": "初始化城市字典"})


class RecordWeatherView(View):
    """ 指定城市天气信息"""
    def get(self, request):
        return HttpResponse("这里展示爬取的天气信息")

    def post(self, request):
        city_name = request.POST.get("city_name") or "北京"
        init_city.get_weather_of_city(city_name)
        return JsonResponse({"info": "爬取天气信息成功"})
