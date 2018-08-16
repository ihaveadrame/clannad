import json
from urllib import request
# from ..models import City, Prov, Town
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
    # full_char, town_id = get_town_info(city_name)
    full_char, town_id = "beijing", "101010100"
    headers = {
        "tid": town_id,
        "wt_city": full_char
    }
    _request = request.Request("http://tianqi.sogou.com", headers=headers)
    response = request.urlopen(_request)
    # 读取内容 并将byte转为string
    content = response.read().decode("utf-8")
    # 获取天气信息
    get_data_from_html(content)


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
        "//span[@class='hundity']"
    )[0].text.replace("<li></li>", "")
    # 温度（最低-最高-当前温度）
    current_temp = html.xpath("//span[@class='num']/text()")[0]
    week_max_temp = html.xpath("//*[@class='r-temp']//@data-high")[0]
    max_temp = str(week_max_temp).split(',')[1]
    week_min_temp = html.xpath("//*[@class='r-temp']//@data-low")[0]
    min_temp = str(week_min_temp).split(',')[1]
    # 空气质量指数
    air_quality_number = html.xpath("//span[@class='liv-text']/a/em/text()")[0]
    # 风向 级别
    
    # 天气
    # 日期
    print(max_temp)
    print(isinstance(current_temp, str))
    print(type(max_temp))
    print(current_temp)
    print(air_quality_number)


if __name__ == "__main__":
    get_weather_of_city("北京")
