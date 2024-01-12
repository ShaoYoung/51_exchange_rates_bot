import requests
import xml.etree.ElementTree as ET
from dateutil.parser import parse
from datetime import datetime

# Дата последнего обновления и курсы валют (для кэширования курсов во время работы бота, т.к. в API есть ограничения)
exchange_rates = {
    'last_updated_datetime': datetime.utcnow().replace(year=2023),
    'exchange_rates': dict()
}


def get_currencies() -> dict:
    # Тестовый возврат обычного словаря
    currencies = {
        'RUR': 'Российский рубль',
        'USD': 'Доллар США',
        'EUR': 'Евро',
        'CHF': 'Швейцарский франк',
        'GBP': 'Британский фунт стерлингов',
        'CAD': 'Канадский доллар',
        'JPY': 'Японская иена',
        'AUD': 'Австралийский доллар',
        'NZD': 'Новозеландский доллар',
    }
    return currencies


def get_course_cbrf(currency: str = 'USD') -> float:
    """
    Курс ЦБ РФ
    :param currency: валюта
    :return: курс валюты к рублю
    """
    valute = f"./Valute[CharCode='{currency}']/Value"
    url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    rate = float(
        ET.fromstring(requests.get(url=url).text).find(valute).text.replace(',', '.'))
    return rate


# Использование API ExchangeRate
# Он поддерживает 161 валюту и предлагает 1500 бесплатных запросов в месяц.
# Кроме того, также есть открытый API, который предлагает ежедневно обновляемые данные.
# Курсы обновляются ежедневно.
# Открытый API не предлагает точный курс обмена.
# Можно бесплатно зарегистрироваться и получить ключ API, чтобы извлекать точные обменные курсы.
def get_all_exchange_rates_erapi(src: str = 'USD') -> dict:
    """
    Получает дату обновления и курсы валют с API er-api.com
    :param src: Базовая валюта
    :return: Словарь. Дата обновления и словарь курсов валют
    """
    global exchange_rates
    # Если дата имеющихся курсов (пока сохраняем в памяти на время работы) меньше текущей даты, то обновляем курсы валют
    if exchange_rates['last_updated_datetime'].date() < datetime.utcnow().date():
        # print('Имеющиеся курсы устарели')
        url = f"https://open.er-api.com/v6/latest/{src}"
        # request the open ExchangeRate API and convert to Python dict using .json()
        data = requests.get(url).json()
        minor_currencies = [
            'MGA', 'ETB', 'VUV', 'ANG', 'GMD', 'STN', 'BSD', 'BBD', 'BZD', 'BND',
            'XCD', 'GYD', 'CVE', 'KYD', 'LRD', 'NAD', 'SBD', 'SRD', 'TTD', 'FJD',
            'AOA', 'UGX', 'MWK', 'GTQ', 'PGK', 'LAK', 'NIO', 'MMK', 'SLL', 'SZL',
            'LSL', 'MZN', 'ERN', 'BTN', 'TOP', 'MOP', 'DOP', 'BWP', 'KHR', 'MUR',
            'SCR', 'GHS', 'BDT', 'WST', 'AWG', 'BIF', 'GNF', 'DJF', 'KMF', 'TVD',
            'CDF', 'RWF', 'XPF', 'XOF', 'XAF', 'SHP', 'SDG', 'FKP', 'KES', 'SOS',
            'SLE', 'MRU'
        ]
        if data["result"] == "success":
            # request successful
            # get the last updated datetime
            exchange_rates['last_updated_datetime'] = parse(data["time_last_update_utc"])
            exchange_rates['exchange_rates'] = data["rates"]
            for minor_currency in minor_currencies:
                exchange_rates['exchange_rates'].pop(minor_currency)
    # else:
        # print('Курсы валют актуальны')

    return exchange_rates


def get_course(first_currency: str, second_currency: str) -> str:
    """
    Определение курса
    :param first_currency: Первая валюта
    :param second_currency: Вторая валюта
    :return: Форматированная строка с результатом
    """
    global exchange_rates
    exchange_rates = get_all_exchange_rates_erapi()
    course = round(exchange_rates['exchange_rates'][second_currency] / exchange_rates['exchange_rates'][first_currency], 4)
    return f'На {exchange_rates["last_updated_datetime"].strftime("%d/%m/%Y, %H:%M:%S")} (UTC)\n<b>Курс {first_currency} / {second_currency} = {course}</b>'


if __name__ == '__main__':
    # print(get_course_cbrf('USD'))
    # last_updated_datetime, exchange_rates = get_all_exchange_rates_erapi('USD')
    # print(last_updated_datetime)
    print(exchange_rates)
    get_all_exchange_rates_erapi()
    print(exchange_rates)
    get_all_exchange_rates_erapi()
    print(exchange_rates)
    print(get_course('USD', 'RUB'))
    print(get_course('CAD', 'CHF'))

