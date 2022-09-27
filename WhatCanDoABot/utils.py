import requests
import json

from config import keys

class ConvertionException(Exception):
    pass

class Converter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}. Будет такая же сумма.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(
                f'Не удалось обработать валюту {quote}. Бот пока не умеет работать с такой валютой.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(
                f'Не удалось обработать валюту {base}. Бот пока не умеет работать с такой валютой.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}. Должно быть число.')

        r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key=507452a90d133eeff4c02a5be7028ca7&symbols={quote_ticker},{base_ticker}')
        total_base = json.loads(r.content)['rates'][base_ticker] / json.loads(r.content)['rates'][quote_ticker] * amount

        return total_base