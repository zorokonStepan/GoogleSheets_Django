from django.db import models


class GoogleTab(models.Model):
    sequence_number = models.IntegerField(unique=True, verbose_name="№")
    order_number = models.IntegerField(primary_key=True, verbose_name="заказ №")
    cost_dollars = models.IntegerField(verbose_name="стоимость, $")
    cost_rubles = models.IntegerField(verbose_name="стоимость, ₽")
    delivery_time = models.DateField(verbose_name="срок поставки")

    class Meta:
        verbose_name_plural = 'Google таблицы'
        verbose_name = 'Google таблица'
        ordering = ['sequence_number']

