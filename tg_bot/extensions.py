from logs import currencies
import requests
import json


# класс для отлова ошибок
class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        # ошибки пользователя
        if quote == base:
            raise ConvertionException(f'невозможно переводить одинаковые валюты{base}')
        try:
            quote_ticker = currencies[quote]
        except KeyError:
            raise ConvertionException(f'не удалось обработать валюту {quote}')

        try:
            base_ticker = currencies[base]
        except KeyError:
            raise ConvertionException(f'не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'не удалось обработать количество {amount}')

        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={currencies[quote]}&tsyms={currencies[base]}')
        total_base = json.loads(r.content)[currencies[base]]
        # подсчет
        total_base = float(amount) * float(total_base)
        total_base = str(total_base)

        return total_base
