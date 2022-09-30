from environs import Env

env = Env()
env.read_env()

# Имя файла, полученного в Google Developer Console с закрытым ключом, вы должны подставить свое
CREDENTIALS_FILE = '../creds.json'

# ID Google Sheets документа
SPREADSHEET_ID = env.str("SPREADSHEET_ID")

# ссылка на ЦБ РФ для получения котировки валют, нужно подставить
# нужную дату в конце в формате дд/мм/гггг
path_cbr = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req='
# адрес для сохранения графика
path_graph = 'monitoring_google_tab/static/monitoring.png'
# период обновления веб-страницы в секундах
reboot_period = 15
