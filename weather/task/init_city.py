import json
from urllib import request
from ..models import City, Prov, Town, Weather
from lxml import etree


class CityNameError(Exception):
    pass


def get_city_data():
    """爬取城市信息"""
    r = request.urlopen('http://tianqi.sogou.com/site/getpos')
    r = r.read()
    data = json.loads(r)
    local_path = "city.json"

    # 这里有三部分： 省-市-镇
    for i in data["prov"]:
        try:
            prov = Prov(pk=i[0], name=i[1], first_char=i[2])
            prov.save()
        except Exception as e:
            print(i)

    for m in data["city"]:
        try:
            city = City(
                pk=m[0],
                name=m[1],
                first_char=m[3],
                prov_id=Prov.objects.get(pk=m[2])
            )
            city.save()
        except Exception as e:
            print(m)

    for k in data["town"]:
        try:
            town = Town(
                pk=k[0],
                name=k[1],
                city_id=City.objects.get(pk=k[2]),
                full_char=k[3],
                first_char=k[4]
            )
            town.save()
        except Exception as e:
            print(k)
    # 本地备份
    with open(local_path, 'w') as f:
        f.write(json.dumps(data))


def get_weather_of_city(city_name):
    full_char, town_id = get_town_info(city_name)
    _request = request.Request("http://tianqi.sogou.com")
    _request.add_header("cookie", "tid=%s;wt_city=%s" % (town_id, full_char))
    _request.add_header("User-Agent", "Mozilla/5.0")
    response = request.urlopen(_request)
    # 读取内容 并将byte转为string
    content = response.read().decode("utf-8")
    # with open("a.html", "w") as f:
    #     f.write(content)
    # 获取天气信息
    weather_info = get_data_from_html(content)
    # 保存信息
    weather_info.update({"town_id": town_id})
    Weather(**weather_info).save()


def get_town_info(city_name):
    """ 通过城市名称获取"""
    town_info = Town.objects.get(name=city_name)
    if not town_info:
        raise CityNameError("不存在区（县）: %s" % city_name)
    return town_info.full_char, town_info.pk


def get_data_from_html(html):
    """从html中提取信息"""
    html = etree.HTML(html)
    # result = etree.tostring(html)
    # 获取空气质量
    air_quality = html.xpath("//p[@class='livindex']/span[last()]/text()")[0]
    # 湿度
    humidity = html.xpath(
        "//span[@class='hundity']/text()"
    )[1].replace("%", "").split(" ")[1]
    # 温度（最低-最高-当前温度）
    current_temp = html.xpath("//span[@class='num']/text()")[0]
    week_max_temp = html.xpath("//*[@class='r-temp']//@data-high")[0]
    max_temp = str(week_max_temp).split(',')[1]
    week_min_temp = html.xpath("//*[@class='r-temp']//@data-low")[0]
    min_temp = str(week_min_temp).split(',')[1]
    # 空气质量指数
    air_quality_number = html.xpath("//span[@class='liv-text']/a/em/text()")[0]
    # 风向 级别
    wind, wind_lv = html.xpath(
        "//span[@class='wind']/text()"
    )[1].strip().split(" ")
    # 天气
    weather = html.xpath(
        """ //div[@pbflag='今日天气']/div[@class='row1']/div[@class='r1-img']/p/text()
        """
    )[0]
    # 日期
    date_p, week, date_n = html.xpath(
        "//div[@pbflag='今日天气']/div[@class='row2 row2-0']/a/text()"
    )[0].strip().split(" ")
    return dict(
        air_quality=air_quality,
        humidity=humidity,
        current_temp=current_temp,
        week_max_temp=week_max_temp,
        week_min_temp=week_min_temp,
        max_temp=max_temp,
        min_temp=min_temp,
        air_quality_number=air_quality_number,
        wind=wind,
        weather=weather,
        wind_lv=wind_lv,
        date_n=date_n,
        date_p=date_p,
        week=week
    )


if __name__ == "__main__":
    get_weather_of_city("北京")
