from enum import StrEnum
import msgspec


# Перечисление для локализации
class Locale(StrEnum):
    """Язык отображения информации."""
    RU_RU = "ru-RU"
    EN_EN = "en-EN"
    EN_US = "en-US"


# Перечисление для типов валют
class Currency(StrEnum):
    """Тип валюты для отображения стоимости товара."""
    RUB = "RUB"  # Российский рубль
    RUR = "RUR"  # Российский рубль

    USD = "USD"  # Доллар США
    EUR = "EUR"  # Евро
    UAH = "UAH"  # Украинская гривна


# Перечисление для типов валют дигиселлера
class CurrencyDigiseller(StrEnum):
    WMZ = 'WMZ'
    WMR = 'WMR'
    WME = 'WME'
    WMX = 'WMX'


# Перечисление для типов опций параметра
class VariantTypes(StrEnum):
    PERCENTPLUS = 'percentplus'
    PERCENTMINUS = 'percentminus'
    PRICEPLUS = 'priceplus'
    PRICEMINUS = 'priceminus'


# Перечисление для типов параметров
class OptionTypes(StrEnum):
    TEXTAREA = "textarea"
    CHECKBOX = "checkbox"
    TEXT = "text"
    RADIO = "radio"
    SELECT = "select"


# Схема сообщения об ошибке
class ErrorMessage(msgspec.Struct, forbid_unknown_fields=True):
    locale: Locale
    value: str


# Схема ошибки
class Error(msgspec.Struct, forbid_unknown_fields=True):
    code: str
    message: list[ErrorMessage] | None


# Базовая схема ответа
class BaseResponse(msgspec.Struct, forbid_unknown_fields=True):
    retval: int
    retdesc: str | None
    errors: list[Error] | None
