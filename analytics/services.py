import requests
import json
import geocoder

from analytics.models import Franchise, Restaurant, City


def _get_data_burger_king() -> None:
    """Получает данные о ресторанах с оф.сайта Burger King и сохраняет в БД"""
    bk = requests.get('https://burgerking.ru/restaurant-locations-json-reply-new/')
    bk_json = json.loads(bk.text)
    restaurant = _check_exists_restaurant_name('Burger King')

    for franchise in bk_json:
        latitube = franchise["latitude"]
        longitube = franchise["longitude"]
        coordinates = f'{latitube}, {longitube}'
        b = _check_exists_franchise(restaurant, coordinates)
        if b:
            continue

        city_name = _reverse_name_city_by_coords(latitube, longitube)
        # city_name = 'None'
        city = _check_exists_city(city_name)

        bk_add = Franchise(restaurant=restaurant, coordinates=coordinates, city=city)
        bk_add.save()


def _get_data_kfc() -> None:
    """Получает данные о ресторанах с оф.сайта KFC (скачанного файла json) и сохраняет в БД"""
    with open('static/json/KFC.json', encoding='utf-8') as f:
        kfc_json = json.loads(f.read())

    restaurant = _check_exists_restaurant_name('KFC')
    for franchise in kfc_json['searchResults']:
        coordinates = f"{franchise['store']['contacts']['coordinates']['geometry']['coordinates'][0]}, " \
                      f"{franchise['store']['contacts']['coordinates']['geometry']['coordinates'][1]}"
        b = _check_exists_franchise(restaurant, coordinates)
        if b:
            continue
        city_name = franchise['store']['contacts']['city']['ru']
        city = _check_exists_city(city_name)

        kfc_add = Franchise(restaurant=restaurant, coordinates=coordinates, city=city)
        kfc_add.save()


def _get_data_mcdonalds() -> None:
    """Получает данные о ресторанах с оф.сайта McDonalds и сохраняет в БД"""
    mc = requests.get('https://mcdonalds.ru/api/restaurants')
    mc_json = json.loads(mc.text)
    restaurant = _check_exists_restaurant_name('McDonalds')

    for franchise in mc_json['restaurants']:

        latitube = franchise['latitude']
        longitube = franchise['longitude']

        coordinates = f"{latitube}, {longitube}"
        b = _check_exists_franchise(restaurant, coordinates)
        if b:
            continue
        try:
            city_name = franchise['location']['name']
        except KeyError:
            city_name = _reverse_name_city_by_coords(latitube, longitube)
        city = _check_exists_city(city_name)

        mc_add = Franchise(restaurant=restaurant, coordinates=coordinates, city=city)
        mc_add.save()


def _check_exists_restaurant_name(name):
    """Ищет в БД ресторан, в случае отстутствия - сохраняет"""
    try:
        restaurant = Restaurant.objects.get(name=name)
    except Restaurant.DoesNotExist:
        restaurant = Restaurant(name=name)
        restaurant.save()
    return restaurant


def _check_exists_franchise(restaurant, coordinates):
    """Проверяет существует ли филиал в БД"""
    for coord in Franchise.objects.filter(restaurant=restaurant):
        if coordinates == coord.coordinates:
            return True


def _check_exists_city(city_name):
    """Проверяет существует ли город в БД"""
    try:
        city = City.objects.get(name__iexact=city_name.title())
    except City.DoesNotExist:
        city = City(name=city_name.title())
        city.save()
    return city


def _reverse_name_city_by_coords(latitube, longitube):
    """Возвращает название города по координатам. (долго!)"""
    city_name = geocoder.reverse([latitube, longitube], 'ArcGIS').city
    if not city_name:
        city_name = 'None'
    return city_name
