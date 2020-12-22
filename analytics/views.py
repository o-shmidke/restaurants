from django.http import HttpResponse
from django.shortcuts import render

import pandas as pd
from django_pandas.io import read_frame

from analytics.models import Franchise, Restaurant
from analytics.services import _get_data_mcdonalds, _get_data_kfc, _get_data_burger_king


def get_data(request):
    """Обновляет данные о ресторанах"""
    _get_data_burger_king()
    _get_data_kfc()
    _get_data_mcdonalds()
    return HttpResponse(f"Загрузка данных прошла успешно. Всего филиалов: "
                        f"KFC: {Franchise.objects.filter(restaurant__name='KFC').count()}; "
                        f"McDonalds: {Franchise.objects.filter(restaurant__name='McDonalds').count()}; "
                        f"Burger King: {Franchise.objects.filter(restaurant__name='Burger King').count()};")


def view_data(request):
    """Отображает список всех ресторанов и проводит анализ конкурентной способности в Москве"""
    all = Franchise.objects.all()

    frame = read_frame(all, fieldnames=['restaurant', 'coordinates', 'city'])
    count_restaurants = frame.groupby(['restaurant'])['city'].count()

    tab1 = frame.loc[(frame['city'] == 'Москва')]
    tab2 = frame.loc[(frame['city'] == 'Москва И Мо')]
    analiz = pd.concat([tab1, tab2]).groupby('restaurant')['city'].count()

    with open('templates/table_of_restaurants.html', 'w', encoding='utf-8') as f:
        f.write(frame.to_html())

    return render(request, 'base.html',
                  {'count_restaurants': count_restaurants.to_dict(), 'analiz': analiz.to_dict()})
