import json
from urllib import request
from ..models import City, Prov, Town


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
