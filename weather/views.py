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
