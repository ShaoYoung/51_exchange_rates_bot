

def get_currencies() -> dict:
    # TODO Сделать запрос доступных валют ЦБ РФ
    # пока возврат обычного словаря
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