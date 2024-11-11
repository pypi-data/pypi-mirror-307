import math


def haversine(lon1, lat1, lon2, lat2):
    # 将角度转化为弧度
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # Haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371 # 地球平均半径，单位为公里
    return c * r


def longrc(lat, lon, width=10):
    longrkm = haversine(lon, lat - width / 2, lon, lat + width / 2)
    longckm = haversine(lon - width / 2, lat, lon + width / 2, lat)
    return longrkm, longckm