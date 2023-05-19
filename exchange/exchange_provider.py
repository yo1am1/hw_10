import abc
import dataclasses
import enum

import requests


class ExchangeCodes(enum.Enum):
    USD = 840
    EUR = 978
    UAH = 980


@dataclasses.dataclass(frozen=True)
class SellBuy:
    sell: float
    buy: float


class ExchangeBase(abc.ABC):
    """
    Base class for exchange providers, should define get_rate() method
    """

    def __init__(self, vendor, currency_a, currency_b):
        self.vendor = vendor
        self.currency_a = currency_a
        self.currency_b = currency_b
        self.pair: SellBuy = None

    @abc.abstractmethod
    def get_rate(self):
        raise NotImplementedError("Method get_rate() is not implemented")


class MonoExchange(ExchangeBase):
    def get_rate(self):
        a_code = ExchangeCodes[self.currency_a].value
        b_code = ExchangeCodes[self.currency_b].value
        r = requests.get("https://api.monobank.ua/bank/currency")
        r.raise_for_status()
        for rate in r.json():
            currency_code_a = rate["currencyCodeA"]
            currency_code_b = rate["currencyCodeB"]
            if currency_code_a == a_code and currency_code_b == b_code:
                self.pair = SellBuy(rate["rateSell"], rate["rateBuy"])

                return


class PrivatExchange(ExchangeBase):
    def get_rate(self):
        r = requests.get(
            "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11"
        )
        r.raise_for_status()
        for rate in r.json():
            if rate["ccy"] == self.currency_a and rate["base_ccy"] == self.currency_b:
                self.pair = SellBuy(float(rate["sale"]), float(rate["buy"]))


class VkurseExchange(ExchangeBase):
    def get_rate(self):
        r = requests.get("http://vkurse.dp.ua/course.json")
        r.raise_for_status()
        for rate in r.json():
            for i in range(len(rate)):
                if self.currency_a == "UAH" and rate[i] == self.currency_b:
                    self.pair = SellBuy(float(rate["sale"]), float(rate["buy"]))
                elif rate[i] == self.currency_b and self.currency_a == "UAH":
                    self.pair = SellBuy(float(rate["buy"]), float(rate["sale"]))


class NBUExchange(ExchangeBase):
    def get_rate(self):
        r = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json")
        r.raise_for_status()
        for rate in r.json():
            if rate["cc"] == self.currency_a and rate["r030"] == ExchangeCodes[self.currency_b].value:
                self.pair = SellBuy(float(rate["rate"]), float(rate["rate"]))


class CurrencyAPIExchange(ExchangeBase):
    def get_rate(self):
        r = requests.get(
            f"https://api.currencyapi.com/v3/latest?apikey=YQeLH52G55DlV361wbi6Vs1cDj3Jg0TG2KTSBIG6&currencies={self.currency_a}%2C{self.currency_b}")
        r.raise_for_status()
        for rate in r.json()["data"]:
            if self.currency_a == "USD" and rate["code"] == self.currency_b:
                self.pair = SellBuy(float(rate["value"]), float(rate["value"]))
