from django.db import models


class Restaurant(models.Model):
    """Модель наименования ресторанов"""
    name = models.CharField(max_length=50, verbose_name='Наименование ресторана')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ресторан'
        verbose_name_plural = "Рестораны"


class City(models.Model):
    """Модель города"""
    name = models.CharField(max_length=50, verbose_name='City')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = "Города"


class Franchise(models.Model):
    """Модель представляющая франшизы/филиалы ресторанов"""
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='Ресторан')
    coordinates = models.CharField(max_length=100, verbose_name='Координаты')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город')

    def __str__(self):
        return f'{self.restaurant.name} - г.{self.city} ({self.coordinates})'

    class Meta:
        verbose_name = 'Франшиза'
        verbose_name_plural = "Франшизы"
