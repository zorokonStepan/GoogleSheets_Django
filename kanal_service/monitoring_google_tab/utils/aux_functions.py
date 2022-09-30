import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


"""Модуль со вспомогательными функциями"""


matplotlib.use('Agg')


def convert_date(d: datetime.date):
    """функция, с помощью которой будет создана векторная функция convert_date_vect
    для преобразования даты из формата БД в формат для вывода на веб страницу"""
    return d.strftime('%d.%m.%Y')


convert_date_vect = np.vectorize(convert_date)  # создание векторной функции


def sorted_dict(data_db: dict, index: int):
    """
    :param data_db: словарь для сортировки формата {key: sequence}
    :param index: индекс sequence по которому будет сортировка производиться
    :return: dict - отсортированный словарь, numpy.ndarray - sequence после сортировки
    начального словаря
    """
    sorted_tuples_data_db = sorted(data_db.items(), key=lambda item: item[1][index])
    sorted_data_db = {k: v for k, v in sorted_tuples_data_db}

    sorted_data_db_values = np.array(tuple(sorted_data_db.values()))

    return sorted_data_db, sorted_data_db_values


def make_graph(data_db: dict, path_graph: str):
    """
    Создание графика по словарю с данными. График сохраняется в виде изображения в
    формате .png по заданному адресу - path_graph
    :param data_db: dict - словарь с данными
    :param path_graph: путь к изображению вместо которого будет создано новое изображениюс графиком
    :return: None
    """
    sorted_data_db, sorted_data_db_values = sorted_dict(data_db, index=3)

    cost_dollars = sorted_data_db_values[:, 1]
    delivery_time = sorted_data_db_values[:, 3]
    # convert date
    delivery_time = convert_date_vect(delivery_time)

    fig, ax = plt.subplots()
    ax.plot(delivery_time, cost_dollars, color='b', linewidth=3)
    # Устанавливаем интервал основных делений:
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(500))

    # Настраиваем вид основных тиков:
    ax.tick_params(axis='x',
                   labelsize=15,  # Размер подписи
                   labelrotation=45)  # Поворот подписей

    ax.tick_params(axis='y',
                   labelsize=15)  # Размер подписи

    ax.grid(axis='y')  # добавить сетку по оси y
    fig.set_figwidth(16)
    fig.set_figheight(12)

    fig.savefig(path_graph, dpi=70)  # сохранить график как .png изображение по адресу path_graph
