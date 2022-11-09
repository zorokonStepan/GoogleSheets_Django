Программа реализует взаимодействие Google Sheets и БД на основе PostgreSQL.
Содержание документа выводиться онлайн на веб-странице с автоматическим обновлением.
Курс валюты берется со официальной ссылки ЦБ РФ.

Выглядит Google Sheet так:
<p align="center">
  <img src="https://github.com/zorokonStepan/GoogleSheets_Django/raw/main/img_git/google_sh.png" width="450" title="GoogleSheet">
</p>

Выглядит веб-страница так:
<p align="center">
  <img src="https://github.com/zorokonStepan/GoogleSheets_Django/raw/main/img_git/new_web_page.png" width="450" title="WebPage">
</p>

Запускаем проект на своей машине:
<ol>
    <li>Клонируем репозиторий git clone https://github.com/zorokonStepan/GoogleSheets_Django</li>
    <li>Переходим в папку с проектом cd GoogleSheets_Django (здесь и далее приводятся команды на машине под win)</li>
    <li>Устанавливаем виртуальное окружение python -m venv venv</li>
    <li>Активируем виртуальное окружение .\venv\Scripts\activate</li>
    <li>Обновляем pip python -m pip install --upgrade pip</li>
    <li>Устанавливаем в виртуальном окружении зависимости для проекта 
        python -m pip install --no-cache-dir -r requirements.txt</li>
    <li>Установить PostgreSQL. Создать БД.</li>
    <li>Создать файл .env и прописать в него данные. в env_example указано какие<br>
        SECRET_KEY= - ключ Django<br>
        SPREADSHEET_ID=ID Google Sheet<br>
        <br>
        Параметры БД:<br>
        NAME=<br>
        USER=<br>
        PASSWORD=<br>
        HOST=<br>
        PORT=<br>
    </li>
    <li>Сделать миграции БД<br>
        cd kanal_service<br>
        python manage.py makemigrations monitoring_google_tab<br>
        python manage.py migrate<br>
        <br></li>
    <li>Загляните в kanal_service\monitoring_google_tab\config.py<br>
        Для Google Sheet:<br>
        CREDENTIALS_FILE =<br>
        SPREADSHEET_ID =<br>
        <br>
        Менять не стоит:<br>
        path_cbr = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req='<br>
        path_graph = 'monitoring_google_tab/static/monitoring.png'<br>
        <br>
        Менять стоит:<br>
        reboot_period = 15  # период обновления веб-страницы в секундах<br>
        <br>
    </li>
    <li>Создать проект в Google<br>
        получить ключи в .json и сохранить как creds.json в корне данного проекта<br>
        пример в creds.json.example<br>
        Подключить к проекту Google Drive API и Google Sheets API и т.д. см:<br>
        https://habr.com/ru/post/483302/<br>
        https://www.youtube.com/watch?v=Bf8KHZtcxnA&t=662s<br>
        https://habr.com/ru/post/575160/<br>
        https://habr.com/ru/post/305378/<br>
        <br>
    </li>
    <li>Запуск локального сервера python manage.py runserver<br></li>
    <li>По адресу http://localhost:8000 будет 
    <img src="https://github.com/zorokonStepan/GoogleSheets_Django/raw/main/img_git/new_web_page.png" width="450" title="WebPage"></li>
</ol>

P.S.
<ol>
    <li>Данная программа написана для обработки Google таблицы определенной формы и содержания.</li>
</ol>


