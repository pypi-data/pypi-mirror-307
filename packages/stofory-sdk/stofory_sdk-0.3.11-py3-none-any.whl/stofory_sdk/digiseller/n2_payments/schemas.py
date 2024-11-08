from enum import StrEnum
from typing import Any, List, Union, Optional, Annotated

import msgspec

from ..schemas import Locale, OptionTypes


# Предварительная проверка параметров
class ProductOption(msgspec.Struct, forbid_unknown_fields=True):
    id: int  # Идентификатор опции
    type: str  # Тип опции, например, текст, чекбокс и т.д.
    value: Union[int, str]  # Значение опции, может быть текстовым или числовым


class CheckParamsRequest(msgspec.Struct, forbid_unknown_fields=True):
    product: dict  # Информация о продукте, включая идентификатор и количество
    options: List[ProductOption]  # Список выбранных параметров продукта


class CheckParamsResponse(msgspec.Struct, forbid_unknown_fields=True):
    error: str  # Сообщение об ошибке, если есть; пустое, если ошибок нет


# Определение значений параметров товара при покупке

class PreliminaryOption(msgspec.Struct, forbid_unknown_fields=True):
    """Схема параметра продукта, где type представляет тип опции, а value — её значение"""
    id: int  # Идентификатор параметра
    type: OptionTypes  # Тип опции (например, текст, чекбокс)
    value: str  # Значение опции, может быть текстом или id выбранного значения для select, checkbox, radio


class IdParametersValuesPurchaseOptions(msgspec.Struct, forbid_unknown_fields=True, tag="id"):
    type = "id"  # Обязательно передавать
    id: int  # ID выбранного значения, применимо для select, checkbox, radio


class TextParametersValuesPurchaseOptions(msgspec.Struct, forbid_unknown_fields=True, tag="text"):
    type = "text"  # Обязательно передавать
    text: Optional[str]  # Текстовое значение, если параметр типа 'text'


# Основная структура с объединением
class SetParametersPurchaseOptions(msgspec.Struct, forbid_unknown_fields=True, tag_field="type"):
    id: int  # ID параметра
    value: Union[
        IdParametersValuesPurchaseOptions,
        TextParametersValuesPurchaseOptions
    ]  # Значение параметра, включая id и/или text


class PurchaseOptionsRequest(msgspec.Struct, forbid_unknown_fields=True):
    product_id: int  # Идентификатор продукта
    options: list[SetParametersPurchaseOptions] = msgspec.UNSET  # Список опций с их значениями
    unit_cnt: Optional[int] = msgspec.UNSET  # Количество товара с динамической ценой
    lang: Locale = Locale.RU_RU  # Язык отображения информации
    ip: str = "0.0.0.0"  # IP-адрес пользователя для дополнительной информации


class PurchaseOptionsResponse(msgspec.Struct, forbid_unknown_fields=True):
    retval: int  # Код выполнения запроса: 0 - успешно
    retdesc: Optional[str]  # Описание результата выполнения
    id_po: int  # Уникальный ID набора значений, используемый для перехода к оплате


# Работа с корзиной
# 1. Добавление товара в корзину

# Перечисление для типа валюты (способа платежа)
class CartTypeCurrency(StrEnum):
    WMR = "WMR"  # WebMoney рубли
    WMZ = "WMZ"  # WebMoney доллары
    WME = "WME"  # WebMoney евро
    WMX = "WMX"  # WebMoney биткоины
    PCR = "PCR"  # Промсвязьбанк
    QSP = "QSP"  # Qiwi
    PYU = "PYU"  # PayU
    RCC = "RCC"  # Российская кредитная карта
    MTS = "MTS"  # МТС
    TL2 = "TL2"  # Тел2
    BLN = "BLN"  # Билайн
    MGF = "MGF"  # Мегафон
    BNK = "BNK"  # Банковский перевод
    GRN = "GRN"  # Гривна


# Перечисление для языка интерфейса
class CartLanguage(StrEnum):
    RU_RU = "ru-RU"  # Русский
    EN_US = "en-US"  # Английский


class CartAddRequest(msgspec.Struct, forbid_unknown_fields=True):
    product_id: int  # Идентификатор продукта
    product_cnt: Annotated[int, msgspec.Meta(ge=1)]  # Количество товаров для добавления
    typecurr: CartTypeCurrency  # Тип валюты
    email: Optional[str] = None  # Email покупателя
    lang: Optional[CartLanguage] = CartLanguage.RU_RU  # Язык для сообщений об ошибках
    cart_uid: Optional[str] = None  # UID корзины
    id_po: Optional[int] = None  # Уникальный ID выбранного набора значений


class CartProductVariant(msgspec.Struct, forbid_unknown_fields=True):
    data: str
    modify: str


class CartProductOptions(msgspec.Struct, forbid_unknown_fields=True):
    id: str
    name: str
    variant: Optional[List[CartProductVariant]] = None


class CartProduct(msgspec.Struct, forbid_unknown_fields=True):
    id: int  # ID товара
    item_id: int  # ID позиции в корзине
    name: str  # Название товара
    name_original: str  # Название товара (ОРИГИНАЛЬНОЕ)
    available: bool  # Доступность для покупки (1 - доступен, 0 - недоступен)
    price: str  # Цена товара
    price_original: str  # Цена товара (ОРИГИНАЛЬНАЯ)
    currency: str  # Валюта товара
    cnt_item: int  # Количество единиц товара в корзине
    cnt_lock: bool  # Ограничение на количество (1 - ограничено, 0 - не ограничено)
    error: Any = None
    options: Optional[List[CartProductOptions]] = None


class CartAddResponse(msgspec.Struct, forbid_unknown_fields=True):
    cart_err: Optional[str]  # Код ошибки выполнения запроса
    cart_cnt: int  # Общее число товаров в корзине
    cart_uid: str  # UID корзины
    currency: str  # Основная валюта корзины
    cart_curr: List[str]  # Допустимые валюты
    products: List[CartProduct] = []  # Список товаров в корзине
    cart_err_num: Optional[Any] = None  # Дополнительный код ошибки (если есть)
    debug: Optional[Any] = None  # Отладочная информация (если есть)


# 2. Получение списка товаров корзины + обновление числа единиц товара в корзине
class CurrencyCartList(StrEnum):
    RUR = "RUR"  # Российский рубль
    USD = "USD"  # Доллар США
    EUR = "EUR"  # Евро
    UAH = "UAH"  # Украинская гривна
    MBTC = "mBTC"  # Украинская гривна


class CartListRequest(msgspec.Struct, forbid_unknown_fields=True):
    cart_uid: str  # Уникальный идентификатор корзины
    cart_curr: Optional[CurrencyCartList] = None  # Валюта для отображения цен
    item_id: Optional[int] = None  # ID товара в корзине (не путать с product_id)
    product_cnt: Optional[int] = None  # Количество единиц товара для обновления
    lang: Optional[CartLanguage] = CartLanguage.RU_RU  # Язык для отображения информации о товарах


class CartListResponse(msgspec.Struct, forbid_unknown_fields=True, kw_only=True):
    cart_err: str  # Код ошибки (0, если ошибок нет)
    cart_cnt: int = None  # Общее количество товаров в корзине
    amount: str = None  # Общая сумма товаров в корзине
    currency: str = None  # Валюта для отображения
    cart_curr: List[str] = None  # Список доступных валют
    products: List[CartProduct] = None  # Список товаров в корзине с деталями (например, id, название, доступность)
    cart_err_num: str | None = None  # Дополнительный код ошибки (если есть)
    cart_err_msg: str | None = None  # Дополнительный код ошибки (если есть)
    debug: Optional[str] = None  # Отладочная информация (если есть)


# Настройка индивидуальных способов оплаты
# 1. Инициализация платежа
class InitPaymentRequest(msgspec.Struct, forbid_unknown_fields=True, kw_only=True):
    invoice_id: int  # Уникальный идентификатор заказа
    amount: float  # Сумма платежа с точностью до двух знаков
    currency: str  # Валюта платежа (например, USD, RUB, EUR)
    description: str  # Описание платежа
    lang: Optional[str] = "ru-RU"  # Язык интерфейса (по умолчанию ru-RU)
    email: Optional[str] = None  # Email покупателя для расчета скидок или уведомлений
    payment_id: int  # Идентификатор выбранного метода оплаты
    return_url: str  # URL для возврата пользователя после завершения платежа


# 2. Обновление статуса платежа
class UpdatePaymentStatusRequest(msgspec.Struct, forbid_unknown_fields=True):
    invoice_id: int  # Номер заказа в системе Digiseller
    amount: float  # Сумма платежа (два знака после запятой, разделитель - точка)
    currency: str  # Валюта платежа (например, USD, RUB, EUR)
    status: str  # Текущий статус платежа (например, paid, wait, canceled)
    signature: str  # Подпись запроса для проверки подлинности
    error: Optional[str] = None  # Текст ошибки, если он присутствует


# 3. Получение статуса платежа
class PaymentStatusRequest(msgspec.Struct, forbid_unknown_fields=True):
    invoice_id: int  # Идентификатор заказа в системе
    seller_id: int  # Идентификатор продавца
    amount: str  # Сумма платежа (строка для точности)
    currency: str  # Валюта платежа (USD, RUB, EUR)
    signature: str  # Подпись запроса


class PaymentStatusResponse(msgspec.Struct, forbid_unknown_fields=True):
    invoice_id: str  # Номер заказа в системе
    amount: str  # Сумма платежа
    currency: str  # Валюта платежа
    status: str  # Статус платежа (paid, wait, canceled и т.д.)
    signature: str  # Подпись ответа для подтверждения
    error: Optional[str]  # Сообщение об ошибке, если есть
    integrator: Optional[str]  # Платежный интегратор
