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
