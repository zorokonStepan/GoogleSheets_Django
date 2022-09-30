Программа реализует взаимодействие Google Sheets и БД на основе PostgreSQL
согласно ТЗ тестового задания.
Содержание документа выводиться онлайн на веб-странице с автоматическим обновлением.
Курс валюты берется со официальной ссылки ЦБ РФ.

Выглядит Google Sheet так:
<p align="center">
  <img src="https://github.com/zorokonStepan/GoogleSheets_Django/raw/main/img_git/google_sh.png" width="450" title="GoogleSheet">
</p>

Выглядит веб-страница так:
<p align="center">
  <img src="https://github.com/zorokonStepan/GoogleSheets_Django/raw/main/img_git/web_page.png" width="450" title="WebPage">
</p>

Порядок действий:
буду писать команды под Windows, под другие ОС в сети информация есть

1. Установить Python
2. Создать папку проекта.
3. Создать в папке виртуальное окружение python -m venv venv
4. Скачать в папку проекта этот Git репозиторий
5. Активировать виртуальное окружение .\venv\Scripts\activate
6. Установить библиотеки Python pip install -r requirements.txt
7. Установить PostgreSQL. Создать БД.
8. Создать файл .env и прописать в него данные. в env_example указано какие
SECRET_KEY= - ключ Django
SPREADSHEET_ID=ID Google Sheet

Параметры БД:
NAME=
USER=
PASSWORD=
HOST
PORT=

9. Загляните в kanal_service\monitoring_google_sh\config.py
Для Google Sheet:
CREDENTIALS_FILE =
SPREADSHEET_ID =

Менять не стоит:
path_cbr = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req='
path_graph = 'monitoring_google_sh/static/monitoring.png'

Менять стоит:
reboot_period = 15  # период обновления веб-страницы в секундах

10.
Создать проект в Google
получить ключи в .json и сохранить как creds.json в корне данного проекта
пример в creds.json.example
Подключить к проекту Google Drive API и Google Sheets API

и т.д.
см:
https://habr.com/ru/post/483302/
https://www.youtube.com/watch?v=Bf8KHZtcxnA&t=662s
https://habr.com/ru/post/575160/
https://habr.com/ru/post/305378/

11.
Запуск проекта python manage.py runserver
На главной и единственной странице веб приложения появится все, что должно появиться.

P.S.
1. Данная программа написана для обработки Google таблицы определенной формы и содержания.

Замечания по работе согласно ТЗ:
1. В ТЗ указано занести в БД данные из Google Sheets без изменений
Завести в PostgreSQL дату в формате дд.мм.гггг не получилось. Искал долго. Но увы.
2. Реализация на Django - это дополнительный пункт. Рядом с Django д.б. React.
Я с React не знаком. Сделал график с помощью matplotlib.