from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from .utils.work_with_data import GoogleSheet, ManagerDB
from .config import path_graph, reboot_period
from .utils.aux_functions import make_graph


# обработка корнего адреса '/'
def monitoring(request: HttpRequest):
    # создание соединения с Google API - создается 1 экземпляр на протежении работы программы
    # подключение к Google листу
    google_sheet = GoogleSheet()
    # Получение заголовка Google листа. Обновление данных заголовка не предусмотренно.
    head_google_sh = google_sheet.head_google_sheet
    # Получение данных с Google листа.
    data_google_sh = google_sheet.get_data_google_sheet()

    # создание объекта db - работа по поиску изменений в Google листе будут производиться
    # с его помощью, для минимизирования количества запросов к БД
    db = ManagerDB()
    db.change_data(data_google_sh)  # обновление БД и data_db

    # получение данных для рендеринга веб-страницы
    sequence_number, order_number, cost_dollars, cost_rubles, delivery_time = db.get_data_db
    total_rub = cost_rubles.sum()
    total_dol = cost_dollars.sum()
    # создание графика для веб-страницы
    make_graph(db.data_db, path_graph=path_graph)

    content_tab = tuple(zip(sequence_number, order_number, cost_dollars, cost_rubles, delivery_time))

    context = {'head_google_sh': head_google_sh,
               'content_tab': content_tab,
               'total_dol': total_dol,
               'total_rub': total_rub,
               'path_graph': path_graph,
               'reboot_period': reboot_period}

    return render(request, 'monitoring.html', context)

