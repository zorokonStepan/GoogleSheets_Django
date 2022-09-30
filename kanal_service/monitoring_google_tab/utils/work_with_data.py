import httplib2
import datetime
import requests
import xml.etree.ElementTree as ET

from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

from ..models import GoogleTab
from ..config import path_cbr, CREDENTIALS_FILE
from ..config import SPREADSHEET_ID
from .aux_functions import sorted_dict, convert_date_vect

"""
Модуль с классами для сбора данных из Google Sheet, проверки данных на изменения
я актуализации данных в БД.
"""


# SPREADSHEET_ID импортируется из config.py, а хрониться ID в скрытом файле .env
# но т.к. этот ключ может понадобиться проверяющему тестовое задание
# выкладываю ID сюда
SPREADSHEET_ID = '1mLIXrG9BuW8vsGIDczUOUq263jBWry0QBFNCSiFNdG0'


class Singleton:
    """
    Класс для создания общего поведения классов - ValuteExRate, GoogleSheet, ManagerDB
    Реализация паттерна Singleton
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance


class ValuteExRate(Singleton):
    """
    class ValuteExRate реализует получение актуального курса валюты с указанного адреса.
    Парсинг данных будет работать только со страницы ЦБ РФ по запросу
    http://www.cbr.ru/scripts/XML_daily.asp?date_req=02/03/2002
    date_req= Date of query (dd/mm/yyyy)

    В классе реализован паттерн Singletone
    """

    def __init__(self, url=path_cbr, ver_date=datetime.datetime.now().strftime('%d/%m/%Y'), id_valute="R01235"):
        """
        :param url: адрес к ресурсу для получения данных, по умолчанию это
        http://www.cbr.ru/scripts/XML_daily.asp?date_req=
        :param ver_date: по умолчанию - текущая дата в формате '%d/%m/%Y'. Для получения данных
        нужен полный uri: url+ver_date
        :param id_valute: идентификатор валюты, по умолчанию задан id доллара США

        self.ver - действительная котировка валюты:
        по каждому uri можно получить данные на определенный день,
        поэтому нет смысла парсить документ более одного раза в день.
        в атрибуте self.ver экземпляра класса при создании сохраняется текущая котеровка
        При каждом вызове метода __call__ экземпляра будет проверяться дата self.ver_date
        и при необходимости обновляться значение self.ver
        """
        self.url = url
        self.id_valute = id_valute
        self.ver_date = ver_date

        self.ver = self.get_valute_ex_rate()

    def __call__(self):
        """
        :return: действительную котировку валюты на текущий момент. см.docstring метода __init__
        """
        current_date = datetime.datetime.now().strftime('%d/%m/%Y')
        if current_date != self.ver_date:  # котировка должна обновляться каждый день
            self.ver_date = current_date
            self.ver = self.get_valute_ex_rate()
        return self.ver

    def get_valute_ex_rate(self, value=0):
        """
        Получение текущего курса валюты
        :param value: значение текущего курса валюты.
        По умолчанию 0. Если не получиться получить данные с ресурса
        метод вернет значение по умолчанию.
        :return: значение текущего курса валюты.
        """
        uri = self.url + self.ver_date

        response = requests.get(uri)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for valute in root.findall('Valute'):
                if valute.attrib['ID'] == self.id_valute:
                    value = valute.find('Value').text
                    value = float(value.replace(',', '.'))
                    break
        return value


class GoogleSheet(Singleton):
    """
    class GoogleSheet реализует взаимодействие с листом Google Sheet
    класс написан под ТЗ, для работы только с одним листом

    В классе реализован паттерн Singletone
    """
    def __init__(self, credentials_file=CREDENTIALS_FILE, spreadsheet_id=SPREADSHEET_ID,
                 scopes=("https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"),
                 ):
        """

        :param credentials_file: имя файла с закрытым ключом, полученного в Google Developer Console
        :param spreadsheet_id: ID Google Sheets документа
        :param scopes: уровень доступа, который получит экземпляр класса от Google API.
        """
        self.credentials_file = credentials_file
        self.spreadsheet_id = spreadsheet_id
        self.scopes = scopes

        self.service = self.connect_google_sheet()
        self.head_google_sheet = self.get_head_google_sheet

    def connect_google_sheet(self):
        """
        Авторизация в Google API и получение экземпляра доступа к API
        :return: service - экземпляр Google API
        """
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, self.scopes)
        # Авторизуемся в системе
        httpAuth = credentials.authorize(httplib2.Http())  # через httpAuth проходят все запросы
        service = discovery.build('sheets', 'v4', http=httpAuth)  # Выбираем работу с таблицами и 4 версию API
        return service

    @property
    def get_head_google_sheet(self):
        """
        Собирает в кортеж названия заголовка google листа
        Метод написан под конкретную страницу, поэтому диапозон  range='A1:D1' нельзя поменять
        и в return row[0], row[1], row[2], 'стоимость, ₽', row[3] добавление 'стоимость, ₽'
        обусловлено ТЗ
        :return: кортеж названий заголовка google листа
        """
        values = self.service.spreadsheets().values().get(
                            spreadsheetId=self.spreadsheet_id,
                            range='A1:D1',
                            majorDimension='ROWS'
                                ).execute()

        if 'values' in values:
            for row in values['values']:
                return row[0], row[1], row[2], 'стоимость, ₽', row[3]
        return '', '', '', '', ''

    def get_data_google_sheet(self, number_start: int = 2, step: int = 30) -> dict:
        """
        Сбор данных с Google Sheet
        :param number_start: по умолчанию равно 2, обусловлено заполнением заданного листа
        number_stop должен быть равен 1, чтобы step задавать кратно 10
        :param step: шаг выборки строк с Google Sheet
        по умолчантю 30, выбран для примера, на практике лучше ставить больше,
        чтобы уменьшить число запросов к Google Sheet
        :return: сдоварь с данными с Google Sheet в виде(псевдословарь для наглядности):
        {"заказ №": ("№", "стоимость, $", "стоимость, ₽", "срок поставки")}
        """
        number_start -= step
        number_stop = 1
        values = {'values': 'pass'}
        data_google_sh = {}
        # получение текущей котировки доллара с ЦБ РФ
        url = path_cbr + datetime.datetime.now().strftime('%d/%m/%Y')
        valute_ex_rate = ValuteExRate(url=url)
        dollar_ex_rate = valute_ex_rate()

        # type(values) == dict, значение строк под ключом 'values', нет значений - нет 'values'
        while 'values' in values:
            number_start += step
            number_stop += step
            # получение порции данных в values
            values = self.service.spreadsheets().values().get(
                                        spreadsheetId=self.spreadsheet_id,
                                        range=f'A{number_start}:D{number_stop}',
                                        majorDimension='ROWS'
                                    ).execute()

            if 'values' in values:
                # чтение последовательно строк данных
                for row in values['values']:
                    # валидация данных
                    # if row - на случай пустой строки в таблице.
                    # Если после пустой строки есть строка с данными - она будет прочитана
                    if row and (row[0].isdigit() and row[1].isdigit() and row[2].isdigit()):
                        try:  # валидация данных ячейки с датой
                            date = [int(i) for i in row[3].split('.')]
                            date = datetime.date(*date[::-1])
                        except ValueError:
                            continue

                        cost_doll = int(row[2])  # "стоимость, $"
                        cost_rub = round(cost_doll * dollar_ex_rate)  # "стоимость, ₽"
                        data_google_sh[int(row[1])] = (int(row[0]), cost_doll, cost_rub, date)
                    else:
                        continue
        return data_google_sh


class ManagerDB(Singleton):
    """
    class ManagerDB реализует работу с моделью БД GoogleTab.
    Для уменьшения числа запросов к БД GoogleTab используется словарь self.data_db
    С помощью self.data_db определяются изменения в Google Sheet и впоследствии на
    основании этих данных вносятся соответствующие корректировки в БД GoogleTab.

    В классе реализован паттерн Singletone
    """
    def __init__(self, DB=GoogleTab):
        """
        :param DB: по умолчанию GoogleTab

        self.data_db - словарь эквивалентный по содержанию БД GoogleTab.
        При создании экземпляра class ManagerDB словарь self.data_db заполняеися данными с БД GoogleTab.
        в виде(псевдословарь для наглядности):
        {"заказ №": ("№", "стоимость, $", "стоимость, ₽", "срок поставки")}
        """

        self.DB = DB
        self.data_db = {row.order_number: (row.sequence_number, row.cost_dollars, row.cost_rubles, row.delivery_time)
                        for row in self.DB.objects.all()}

    def change_data(self, data_google_sh: dict):
        """
        Для уменьшения числа запросов к БД GoogleTab используется словарь self.data_db
        С помощью self.data_db определяются изменения в Google Sheet и впоследствии на
        основании этих данных вносятся соответствующие корректировки в БД GoogleTab.
        Производится поиск новых, удаленных и измененных данных
        :param data_google_sh: актуальные данные из Google Sheet
        :return: flag True
        """
        # проверить каких данных нет в self.data_db,
        # т.е. новые, каких не стало, какие остались - проверить не изменились ли они
        data_google_sh_keys = set(data_google_sh.keys())
        data_db_keys = set(self.data_db.keys())

        new_data = data_google_sh_keys - data_db_keys
        old_data = data_google_sh_keys & data_db_keys
        deleted_data = data_db_keys - data_google_sh_keys

        # данные, которых больше нет - удалить
        for num in deleted_data:
            _ = self.data_db.pop(num)
            gt = self.DB.objects.get(pk=num)
            gt.delete()

        # проверить на изменение данных в строках которые были с прошлого раза
        for num in old_data:
            if self.data_db[num] != data_google_sh[num]:
                self.data_db[num] = data_google_sh[num]
                gt = self.DB.objects.get(pk=num)
                gt.sequence_number = self.data_db[num][0]
                gt.cost_dollars = self.data_db[num][1]
                gt.cost_rubles = self.data_db[num][2]
                gt.delivery_time = self.data_db[num][3]
                gt.save()

        # добавить новые данные
        for num in new_data:
            self.data_db[num] = data_google_sh[num]
            self.DB.objects.get_or_create(sequence_number=self.data_db[num][0],
                                          defaults={
                                                    'order_number': num,
                                                    'cost_dollars': self.data_db[num][1],
                                                    'cost_rubles': self.data_db[num][2],
                                                    'delivery_time': self.data_db[num][3]
                                            }
                                        )
        return True

    @property
    def get_data_db(self):
        """
        Для более быстрого сбора данных, для исключения итерации данных
        используется библиотека numpy, ее срезы и векторные операции
        для конвертации даты применяется векторная функция convert_date_vect
        :return:
        """
        sorted_data_db, sorted_data_db_values = sorted_dict(self.data_db, index=0)

        sequence_number = sorted_data_db_values[:, 0]
        order_number = tuple(sorted_data_db.keys())
        cost_dollars = sorted_data_db_values[:, 1]
        cost_rubles = sorted_data_db_values[:, 2]
        delivery_time = sorted_data_db_values[:, 3]
        # convert date
        delivery_time = convert_date_vect(delivery_time)

        return sequence_number, order_number, cost_dollars, cost_rubles, delivery_time
