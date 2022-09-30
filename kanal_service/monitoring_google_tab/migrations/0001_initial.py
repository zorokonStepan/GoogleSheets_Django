# Generated by Django 4.1.1 on 2022-09-28 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleTab',
            fields=[
                ('sequence_number', models.IntegerField(unique=True, verbose_name='№')),
                ('order_number', models.IntegerField(primary_key=True, serialize=False, verbose_name='заказ №')),
                ('cost_dollars', models.IntegerField(verbose_name='стоимость, $')),
                ('cost_rubles', models.FloatField(verbose_name='стоимость, ₽')),
                ('delivery_time', models.DateField(verbose_name='срок поставки')),
            ],
            options={
                'verbose_name': 'Google таблица',
                'verbose_name_plural': 'Google таблицы',
                'ordering': ['sequence_number'],
            },
        ),
    ]
