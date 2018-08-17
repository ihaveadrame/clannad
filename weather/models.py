"""天气相关的所有模型"""
from django.db import models


class Prov(models.Model):
    """省份表"""
    name = models.CharField(max_length=20, null=False)
    first_char = models.CharField(max_length=1, null=False)

    def __str__(self):
        return self.name


class City(models.Model):
    """城市表"""
    name = models.CharField(max_length=20, null=False)
    first_char = models.CharField(max_length=1, null=False)
    prov_id = models.ForeignKey(Prov, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Town(models.Model):
    """乡镇表"""
    name = models.CharField(max_length=20, null=False)
    first_char = models.CharField(max_length=1, null=False)
    full_char = models.CharField(max_length=100, null=False)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Weather(models.Model):
    """ 天气信息表"""
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    air_quality = models.CharField(
        "空气质量", max_length=10, null=False, default=""
    )
    air_quality_number = models.IntegerField("空气质量指数", null=False, default=0)
    humidity = models.IntegerField("湿度", null=False, default=0)
    current_temp = models.IntegerField("当前温度", null=False, default=0)
    max_temp = models.IntegerField("最高温度", null=False, default=0)
    min_temp = models.IntegerField("最低温度", null=False, default=0)
    week_max_temp = models.CharField("昨天起7天最高温度", max_length=50, null=False, default="")
    week_min_temp = models.CharField("昨天起7天最低温度", max_length=50, null=False, default="")
    wind = models.CharField("风向", max_length=10, null=False, default="")
    wind_lv = models.CharField("风力", max_length=10, null=False, default="")
    weather = models.CharField("天气", max_length=10, null=False, default="")
    date_p = models.DateField("公历", null=False, auto_now=True)
    date_n = models.CharField("农历", max_length=10, null=False, default="")
    week = models.CharField("星期", max_length=10, null=False, default="")
    create_time = models.DateTimeField("创建时间", null=False, auto_now=True)
