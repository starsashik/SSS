import math

import requests

API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


def geocode(address):
    geocoder_request = f'http://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}' \
                       f'&geocode={address}&format=json'
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    if toponym:
        return toponym
    return 0


def get_coordinates(address):
    toponym = geocode(address)
    if not toponym:
        return None, None
    toponym_coodrinates = toponym["Point"]["pos"]
    top_long, top_latt = toponym_coodrinates.split(' ')
    return float(top_long), float(top_latt)


def get_ll(addrress):
    toponym = geocode(addrress)
    if not toponym:
        return None, None
    toponym_coodrinates = toponym["Point"]["pos"]
    top_long, top_latt = toponym_coodrinates.split(' ')
    ll = f'{top_long},{top_latt}'

    envelope = toponym['boundedBy']['Envelope']
    l, b = envelope['lowerCorner'].split(' ')
    r, t = envelope['upperCorner'].split(' ')
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(b) - float(t)) / 2.0
    spn = f'{dx},{dy}'
    return ll, spn


def ll_distance(x, y):
    degree_to_metr = 111 * 1000
    long_x, lat_x = map(float, x.split(','))
    long_y, lat_y = map(float, y.split(','))

    radians_lattitude = math.radians((lat_x + lat_y) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    dx = abs(long_x - long_y) * degree_to_metr * lat_lon_factor
    dy = abs(lat_x - lat_y) * degree_to_metr

    dist = math.sqrt(dx ** 2 + dy ** 2)

    return dist
