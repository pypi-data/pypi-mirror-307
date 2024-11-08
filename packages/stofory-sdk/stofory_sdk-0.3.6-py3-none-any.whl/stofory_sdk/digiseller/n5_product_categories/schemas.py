from datetime import datetime
from enum import StrEnum, IntEnum
from typing import Annotated, Any, Optional, List, Union, Literal

import msgspec
from msgspec import Meta

from ..lib import BaseStruct
from ..schemas import Locale, Currency, CurrencyDigiseller, OptionTypes


# Перечисление для сортировки
class SortOrder(StrEnum):
    """Тип сортировки для списка товаров."""
    NAME = "name"  # Сортировка по названию
    NAME_DESC = "nameDESC"  # Обратная сортировка по названию
    PRICE = "price"  # Сортировка по цене
    PRICE_DESC = "priceDESC"  # Обратная сортировка по цене


class CategoriesRequest(BaseStruct, forbid_unknown_fields=True):
    """Запрос на получение списка категорий товаров."""

    # Идентификатор категории (целое число, по умолчанию 0 для выбора всего дерева каталога)
    category_id: Annotated[
        int,
        Meta(
            description="Идентификатор категории (целое число, по умолчанию 0 для выбора всего дерева каталога)"
        )
    ] = 0  # По умолчанию выбирается все дерево каталога

    # Язык отображения информации (по умолчанию ru-RU)
    lang: Annotated[
        Locale,
        Meta(description="Язык отображения информации (по умолчанию ru-RU)")
    ] = Locale.RU_RU


class Subcategory(msgspec.Struct, forbid_unknown_fields=True):
    id: int  # Идентификатор подкатегории (целое число)
    name: str  # Название подкатегории (строка)
    cnt: int  # Количество товаров в подкатегории (целое число)


class Category(msgspec.Struct, forbid_unknown_fields=True):
    id: str  # Идентификатор категории (целое число)
    name: str  # Название категории (строка)
    cnt: str  # Количество товаров в категории (целое число)
    sub: Optional[List[Subcategory]] = None


class CategoriesResponse(msgspec.Struct, forbid_unknown_fields=True):
    retval: int  # Код выполнения запроса (целое число)
    retdesc: Optional[str] = None  # Расшифровка кода выполнения запроса (строка)
    category: List[Category] = None  # Список категорий магазина (список объектов Category)
    queryId: Any = None  # я хз что это


# Запрос на получение товаров из категории
class ProductsRequest(BaseStruct, forbid_unknown_fields=True, kw_only=True):
    """Запрос на получение списка товаров в категории."""

    # Идентификатор категории (обязательное поле)
    category_id: Annotated[
        int,
        Meta(
            ge=-3,  # Минимальное значение -3 (популярные товары)
            le=0,  # Максимальное значение 0 (товары на главной странице)
            description="""
                Идентификатор категории:
                0 - товары на главной странице,
                -1 - товары со знаком 'скидка',
                -2 - товары со знаком 'новинка',
                -3 - товары со знаком 'популярный'
            """
        )
    ] = 0  # По умолчанию - товары на главной странице

    # Номер страницы (по умолчанию 1)
    page: Annotated[
        int,
        Meta(
            ge=1,  # Минимальное значение 1
            description="Номер страницы (по умолчанию 1)"
        )
    ] = 1

    # Количество строк на странице (по умолчанию 20, максимум 500)
    rows: Annotated[
        int,
        Meta(
            ge=20,  # Минимальное значение 20
            le=500,  # Максимальное значение 500
            description="Количество строк на странице (по умолчанию 20, максимум 500)"
        )
    ] = 20

    # Способ сортировки товаров (необязательное поле)
    order: Union[SortOrder, msgspec.UNSET] = msgspec.UNSET

    # Валюта отображения стоимости товаров (необязательное поле)
    currency: Annotated[
        Optional[Currency],
        Meta(description="Тип валюты для отображения стоимости товара: USD, RUB, EUR, UAH")
    ] = Currency.RUB

    # Язык отображения информации (по умолчанию ru-RU)
    lang: Annotated[
        Optional[Locale],
        Meta(description="Язык отображения информации (по умолчанию ru-RU)")
    ] = Locale.RU_RU


# Данные о распродаже товара
class SaleInfo(msgspec.Struct, forbid_unknown_fields=True):
    """Информация о распродаже товара."""
    common_base_price: Optional[float] = None  # Базовая стоимость товара до распродажи
    common_price_usd: Optional[float] = None  # Цена до распродажи в долларах США
    common_price_rur: Optional[float] = None  # Цена до распродажи в рублях
    common_price_eur: Optional[float] = None  # Цена до распродажи в евро
    common_price_uah: Optional[float] = None  # Цена до распродажи в гривнах
    sale_begin: Optional[float] = None  # Дата начала распродажи
    sale_end: Optional[float] = None  # Дата окончания распродажи
    sale_percent: Optional[float] = None  # Процент скидки на товар


# Ответ по каждому товару в категории
class ProductResponse(msgspec.Struct, forbid_unknown_fields=True, kw_only=True):
    """Ответ с информацией о товаре в категории."""
    id: str  # Идентификатор товара
    name: str  # Название товара
    cntImg: Optional[int]  # Количество изображений товара (необязательное поле)
    info: Optional[str] = None  # Описание товара (необязательное поле)
    price: str  # Стоимость товара
    base_price: str  # Цена в базовой валюте, установленной продавцом
    base_currency: CurrencyDigiseller  # Базовая валюта, в которой установлена цена товара
    currency: Currency  # Валюта отображения стоимости товара
    price_rub: str  # Стоимость товара в рублях
    price_usd: str  # Стоимость товара в долларах США
    price_eur: str  # Стоимость товара в евро
    price_uah: str  # Стоимость товара в гривнах
    partner_comiss: str  # Партнерская комиссия (в процентах)
    agency_id: str  # Идентификатор партнера
    collection: Optional[str] = None  # Тип содержимого товара (необязательное поле)
    is_available: int  # Наличие товара (0 - отсутствует, 1 - в наличии)
    has_discount: int  # Скидка постоянным покупателям (0 - нет скидки, 1 - есть скидка)
    id_present: int  # ID товара-подарка (0 - подарок не задан)
    sale_info: Optional[SaleInfo] = None  # Информация о распродаже товара (необязательное поле)
    label: Optional[str] = None  # Метка товара (скидка, новинка и т.д., необязательное поле)


# Полный ответ на запрос списка товаров в категории
class ProductsResponse(msgspec.Struct, forbid_unknown_fields=True):
    """Ответ на запрос получения списка товаров в категории."""
    retval: int  # Код выполнения запроса (0 - запрос выполнен)
    retdesc: Optional[str] = None  # Расшифровка кода выполнения запроса
    lang: Optional[str] = None  # Язык отображения информации
    total_pages: int = msgspec.field(name='totalPages', default=None)  # Общее количество страниц
    total_items: int = msgspec.field(name='totalItems', default=None)  # Общее количество товаров
    bread_crumbs: List[dict] = msgspec.field(name='breadCrumbs',
                                             default=None)  # Хлебные крошки - путь к выбранной категории
    categories: List[dict] = None  # Список подкатегорий
    product: List[ProductResponse] = None  # Список товаров в категории
    queryId: Any = None  # Ну не ебу я что это


class ProductsDescriptionRequest(BaseStruct, forbid_unknown_fields=True):
    """Схема запроса для получения описаний товаров по их ID."""
    ids: List[int]  # Идентификаторы товаров (максимум 2000)
    lang: Locale = Locale.RU_RU  # Язык отображения информации, по умолчанию 'ru-RU'


class ProductDescription(msgspec.Struct, forbid_unknown_fields=True, kw_only=True):
    """Ответ с информацией о каждом товаре."""
    id: int  # Идентификатор товара
    id_seller: int  # Идентификатор продавца
    name: str  # Название товара
    info: Optional[str] = ""  # Описание товара (опционально)
    add_info: Optional[str] = ""  # Дополнительная информация о товаре (опционально)
    collection: Optional[str] = ""  # Вид содержимого товара (digi, pins, unit, book, soft)
    base_currency: CurrencyDigiseller  # Базовая валюта
    base_price: float  # Цена в базовой валюте, установленной продавцом
    price_usd: float  # Цена в USD
    price_rub: float  # Цена в RUB
    price_eur: float  # Цена в EUR
    price_uah: float  # Цена в UAH
    cnt_sell: int  # Количество продаж (-1 означает полностью скрыто)
    cnt_sell_hidden: int  # Режим отображения числа продаж (0 - продажи открыты, 1 - скрыты)
    cnt_return: int  # Количество возвратов (-1 означает полностью скрыто)
    cnt_return_hidden: int  # Режим отображения возвратов (0 - возвраты открыты, 1 - скрыты)
    in_stock: int  # Доступность товара (0 - товар отсутствует, 1 - в наличии)
    um_in_stock: Optional[int] = None  # Доступное количество на складе
    num_in_lock: Optional[int] = None  # Количество товаров, зарезервированных под оплату
    owner_id: int  # Код торговой площадки
    release_date: Optional[datetime] = None  # Дата релиза (может быть null)
    sale_info: Optional[SaleInfo] = None  # Информация о распродаже (опционально)


class ProductsDescriptionResponse(msgspec.Struct, forbid_unknown_fields=True):
    """Ответ с информацией о нескольких товарах."""
    products: List[ProductDescription]  # Список товаров


class ProductDescriptionRequest(BaseStruct, forbid_unknown_fields=True):
    """Схема запроса для получения описания товара по его ID."""
    product_id: int  # Идентификатор товара
    partner_uid: Optional[str] = None  # Партнерский UID для учета индивидуальных отчислений
    currency: Optional[Currency] = Currency.RUB  # Валюта отображения цены товара (по умолчанию USD)
    lang: Optional[Locale] = Locale.RU_RU  # Язык отображения информации (по умолчанию ru-RU)
    owner: Optional[int] = None  # Признак отображения всех способов оплаты (1 - показать)
    showHiddenVariants: Optional[int] = None  # Признак отображения всех вариантов параметров (1 - показать)


class CurrencyPrice(msgspec.Struct, forbid_unknown_fields=True):
    """Содержит цены в разных валютах."""
    RUB: float  # Цена в рублях
    USD: float  # Цена в долларах США
    EUR: float  # Цена в евро
    UAH: float  # Цена в гривнах
    mBTC: Optional[float] = None  # Цена в mBTC (миллибиткойн), если доступно
    mLTC: Optional[float] = None  # Цена в mLTC (миллилиткойн), если доступно


class PaymentLimit(msgspec.Struct, forbid_unknown_fields=True):
    """Ограничения способа оплаты."""
    min: Optional[float] = None  # Минимальная сумма платежа
    max: Optional[float] = None  # Максимальная сумма платежа
    currency: Optional[str] = None  # Валюта, в которой действует ограничение


class PaymentCurrency(msgspec.Struct, forbid_unknown_fields=True):
    """Информация о валюте и цене для определенного способа оплаты."""
    currency: str  # Валюта платежа
    code: str  # Код способа оплаты
    price: Optional[float] = None  # Цена в указанной валюте
    limit: Optional[PaymentLimit] = None  # Ограничения на сумму платежа


class PaymentMethod(msgspec.Struct, forbid_unknown_fields=True):
    """Информация о способе оплаты."""
    name: str  # Название способа оплаты
    currencies: List[PaymentCurrency]  # Список валют для этого способа оплаты
    code: Optional[str] = None  # Код метода оплаты (его не было)
    hide: Optional[int] = None  # Параметр для скрытия метода оплаты (его не было)


class PricesUnit(msgspec.Struct, forbid_unknown_fields=True, kw_only=True):
    """Информация о цене и единицах товара."""
    unit_name: str  # Название единицы товара
    unit_amount: float  # Количество единиц товара
    unit_amount_desc: str  # Описание единицы товара
    unit_currency: str  # Валюта для единицы товара
    unit_cnt: float  # Количество единиц товара
    unit_cnt_min: int  # Минимальное количество единиц, которое можно купить
    unit_cnt_max: int  # Максимальное количество единиц, которое можно купить
    unit_cnt_desc: Optional[str]  # Описание количества единиц товара
    unit_fixed: Optional[List[int]] = None  # Фиксированные значения количества единиц
    unit_only_int: Optional[int] = None  # Только целое количество (не дробное)


class PreviewImage(msgspec.Struct, forbid_unknown_fields=True):
    """Предварительное изображение товара."""
    id: int  # Идентификатор изображения
    url: str  # URL изображения
    width: int  # Ширина изображения в пикселях
    height: int  # Высота изображения в пикселях


class PreviewVideoType(StrEnum):
    """Типы предварительного видео."""
    VIDEO = "video"
    YOUTUBE = "youtube"
    VIMEO = "vimeo"


class PreviewVideo(msgspec.Struct, forbid_unknown_fields=True):
    """Предварительное видео товара."""
    type: PreviewVideoType  # Тип видео (youtube, vimeo, etc.)
    id: str  # Идентификатор видео
    preview: str  # URL предварительного изображения для видео


class TextProduct(msgspec.Struct, forbid_unknown_fields=True):
    """Информация о продукте в текстовом формате."""
    date: datetime  # Дата размещения текста
    size: int  # Количество символов текста


class FileProduct(msgspec.Struct, forbid_unknown_fields=True):
    """Информация о продукте в формате файла."""
    date: datetime  # Дата размещения файла
    size: int  # Размер файла в байтах
    name: str  # Имя файла
    trial: Optional[int] = None  # Пробная версия (если доступно)


class Breadcrumb(msgspec.Struct, forbid_unknown_fields=True):
    """Хлебные крошки для навигации по категориям."""
    id: int  # Идентификатор категории
    name: str  # Название категории
    products_cnt: int  # Количество товаров в категории


class Discount(msgspec.Struct, forbid_unknown_fields=True):
    """Информация о скидке на товар."""
    summa: float  # Пороговое значение для скидки
    percent: float  # Процент скидки


class UnitDiscount(msgspec.Struct, forbid_unknown_fields=True):
    """Скидка на товар, рассчитанная на единицу."""
    desc: str  # Описание скидки
    percent: float  # Процент скидки
    price: float  # Цена с учетом скидки


class Units(msgspec.Struct, forbid_unknown_fields=True):
    """Информация о товаре с переменной ценой или моделью 'плати сколько хочешь'."""
    desc: str  # Описание единицы товара
    price: float  # Цена за единицу товара
    discounts: Optional[List[UnitDiscount]] = None  # Список скидок на товар


class Present(msgspec.Struct, forbid_unknown_fields=True):
    """Информация о подарке."""
    id: int  # Идентификатор подарка
    name: str  # Название подарка


class OptionVariantModifyType(StrEnum):
    PERCENT = "%"
    USD = "USD"
    RUB = "RUB"
    EUR = "EUR"
    UAH = "UAH"


class OptionVariant(msgspec.Struct, forbid_unknown_fields=True, kw_only=True):
    """Вариант значения параметра товара."""
    value: int  # Значение варианта
    text: str  # Название варианта
    default: Optional[int] = None  # Значение по умолчанию
    modify: Optional[str] = None  # Изменение цены товара при выборе варианта
    modify_type: Optional[OptionVariantModifyType] = None  # Тип изменения цены (% или фиксированное значение)
    modify_value: Optional[float] = None  # Значение изменения цены
    modify_value_default: Optional[float] = None  # Значение изменения цены по умолчанию
    num_in_stock: Optional[int] = None  # Количество товара на складе
    visible: int  # Параметр видимости 1 - не скрыт иначе - скрыт


class Option(msgspec.Struct, forbid_unknown_fields=True):
    """Параметры, определяемые покупателем при оплате."""
    name: str  # Имя параметра
    label: str  # Метка параметра
    comment: str  # Описание параметра
    type: OptionTypes  # Тип параметра (checkbox, text, radio, etc.)
    separate_content: int  # Признак наличия раздельного содержимого
    required: int  # Обязателен ли параметр
    modifier_visible: int  # Показ модификатора цены
    variants: List[OptionVariant]  # Список вариантов значений


class Statistics(msgspec.Struct, forbid_unknown_fields=True):
    """Статистика по продажам товара."""
    sales: int  # Количество продаж
    sales_hidden: int  # Параметр скрытия количества продаж
    refunds: int  # Количество возвратов
    refunds_hidden: int  # Параметр скрытия количества возвратов
    good_reviews: int  # Количество положительных отзывов
    good_reviews_hidden: int  # Параметр скрытия положительных отзывов
    bad_reviews: int  # Количество отрицательных отзывов
    bad_reviews_hidden: int  # Параметр скрытия отрицательных отзывов


class Seller(msgspec.Struct, forbid_unknown_fields=True):
    """Информация о продавце товара."""
    id: int  # Идентификатор продавца
    name: str  # Имя продавца


class Collection(StrEnum):
    """Тип коллекции товара."""
    BOOK = "book"  # Электронная книга
    DIGI = "digi"  # Цифровой товар
    PINS = "pins"  # Пин-коды
    SOFT = "soft"  # Программа
    UNIT = "unit"  # Товар с нефиксированной ценой


class ProductType(StrEnum):
    TEXT = "text"
    FILE = "file"


class Prices(msgspec.Struct, forbid_unknown_fields=True):
    """Цены товара."""
    initial: CurrencyPrice  # Базовая цена товара
    default: CurrencyPrice  # Цена основного способа оплаты


class Product(msgspec.Struct, forbid_unknown_fields=True, kw_only=True):
    """Информация о товаре."""
    id: int  # Идентификатор товара
    id_prev: int  # Идентификатор предыдущего товара в категории
    id_next: int  # Идентификатор следующего товара в категории
    name: str  # Название товара
    price: float = None  # Цена товара
    currency: Currency  # Валюта товара
    url: Optional[str]  # URL товара
    info: Optional[str] = None  # Описание товара
    add_info: Optional[str] = None  # Дополнительная информация о товаре
    release_date: Optional[str] = None  # Дата релиза товара
    agency_fee: float  # Агентское вознаграждение
    agency_sum: float  # Сумма агентского вознаграждения
    agency_id: Optional[int] = None  # Идентификатор агента
    collection: Collection  # Коллекция товара
    property_good: Annotated[
        int, Meta(ge=1, le=2, description="1 - универсальное, 2 - уникальное")
    ] = msgspec.field(name='propertygood')  # Тип содержимого товара
    is_available: Annotated[
        int, Meta(ge=0, le=1, description="0 - товар отсутствует, 1 - товар в наличии")
    ]  # Доступность товара
    show_rest: Annotated[
        int, Meta(ge=0, le=1, description="0 - скрыт, 1 - отображается остаток")
    ]  # Отображение остатка

    num_in_stock: Optional[int] = None  # Доступное количество товара на складе
    num_in_lock: int  # Количество товаров, зарезервированных под оплату
    pwyw: Optional[int] = None  # Параметр "плати сколько хочешь"
    label: Optional[str] = None  # Метка товара
    prices: Optional[Prices] = None  # Цены товара

    payment_methods: List[PaymentMethod]  # Способы оплаты
    prices_unit: Optional[PricesUnit] = None  # Цены за единицу товара
    preview_imgs: List[PreviewImage] = None  # Изображения товара для предпросмотра
    preview_videos: Optional[List[PreviewVideo]] = None  # Видео товара для предпросмотра

    type: ProductType  # Тип товара
    text: Optional[TextProduct] = None  # Параметры для текстовых товаров
    file: Optional[FileProduct] = None  # Параметры для файловых товаров
    category_id: int  # Идентификатор категории товара
    breadcrumbs: List[Breadcrumb]  # Навигация по категориям
    discounts: List[Discount]  # Скидки на товар
    units: Optional[Units] = None  # Сведения о единицах товара

    present: Optional[Present] = None  # Информация о подарке
    gift_commiss: Optional[float] = None  # Комиссия на подарок
    options: List[Option]  # Параметры товара для выбора при оплате
    options_check: Annotated[
        int,
        Meta(ge=0, le=1,
             description="""
                индикатор включенной опции 
                "перед оплатой отправлять параметры на мой сервер для проверки" 
                (определяется в Параметрах товара)
                """
             )
    ]  # Параметр проверки опций перед оплатой
    statistics: Statistics  # Статистика по товару
    seller: Seller  # Информация о продавце товара
    sale_info: Optional[SaleInfo] = None  # Информация о распродаже

    # Хуй ебу что это
    owner: Any = None
    section_id: Any = None
    no_cart: Any = None
    type_good: Any = None
    discounts: Any = None
    options: Any = None


class ProductDescriptionResponse(msgspec.Struct, forbid_unknown_fields=True, kw_only=True):
    """Ответ API с полной информацией о товаре."""
    retval: int  # Код выполнения запроса
    retdesc: Optional[str] = None  # Описание кода выполнения запроса
    product: Product = None  # Описание товара
    queryId: Optional[Any] = None  # Идентификатор запроса, если доступен


class ProductPriceRequest(BaseStruct, forbid_unknown_fields=True):
    """Схема запроса для получения цены товара с учетом различных параметров."""

    # Идентификатор товара, который необходимо передать для получения цены.
    product_id: Annotated[
        int,
        Meta(
            description="Идентификатор товара"
        )
    ]
    # Опциональный список строк, каждая строка представляет собой пару optionId:valueId.
    # Например, options[]=28532:41541 для передачи значимых параметров, влияющих на цену товара.
    # "options[]": ["28532:41541", "28530:41534"]
    options: Annotated[
        List[str],
        Meta(
            description="Перечисление пар optionId:valueId, например, options[]=28532:41541&options[]=28530:41534"
        )
    ]

    # Опциональная строка, представляющая код валюты. Например, WMR, WMZ и другие трехзначные коды валют.
    currency: Annotated[
        str,
        Meta(
            description="Валюта, трехзначный код метода оплаты (WMR | WMZ | ... )"
        )
    ]

    # Опциональное поле для указания стоимости, которая рассчитывается исходя из указанного количества единиц товара.
    amount: Annotated[
        float,
        Meta(
            description="Стоимость, исходя из указанного количества единиц товара"
        )
    ] = msgspec.UNSET

    # Опциональное поле для указания количества товара с нефиксированной ценой.
    # Обязательный параметр для товаров с нефиксированной ценой.
    unit_cnt: Annotated[
        Optional[int],
        Meta(
            description="Количество товара с нефиксированной ценой, обязателен для товара с нефиксированной ценой"
        )
    ] = msgspec.UNSET

    # Опциональное поле для указания количества товара с фиксированной ценой.
    count: Annotated[
        Optional[int],
        Meta(
            description="Количество товара с фиксированной ценой"
        )
    ] = msgspec.UNSET


class ProductPriceData(msgspec.Struct, forbid_unknown_fields=True):
    """Данные о цене товара."""
    price: Optional[float] = None  # Цена товара в базовой валюте
    count: Optional[float] = None  # Количество единиц товара, исходя из указанной стоимости
    amount: Optional[float] = None  # Стоимость, исходя из указанного количества единиц товара
    currency: Optional[str] = None  # Тип валюты
    commission: Optional[float] = None  # Комиссия в зависимости от способа оплаты
    free_pay: Any = None
    sale_info: Optional[SaleInfo] = None  # Информация о распродаже


class ProductPriceResponse(msgspec.Struct, forbid_unknown_fields=True):
    """Ответ API с информацией о цене товара."""
    retval: int  # Код выполнения запроса (0 - успех, 1 и другие - ограничения)
    retdesc: Optional[str] = None  # Описание кода выполнения запроса
    data: Optional[ProductPriceData] = None  # Данные о цене товара


class ReviewType(StrEnum):
    GOOD = "good"
    BAD = "bad"
    ALL = "all"


class OwnerID(IntEnum):
    OWN_SHOP = 0  # собственный магазин
    PLATI_MARKET = 1  # plati.market
    GGESEL = 1271  # ggesel
    WMCENTER = 9295  # wmcenter.net


class ProductReviewsRequest(BaseStruct, forbid_unknown_fields=True, kw_only=True):
    product_id: Optional[int] = msgspec.UNSET  # Идентификатор товара (необязательный параметр)
    type: ReviewType  # Тип отзыва: good, bad, all
    owner_id: Optional[OwnerID] = OwnerID.OWN_SHOP  # Идентификатор торговой площадки
    page: Optional[int] = 1  # Номер страницы (по умолчанию 1)
    rows: Optional[int] = 20  # Количество строк на странице (по умолчанию 20)
    lang: Optional[Locale] = Locale.RU_RU  # Язык отображения информации (по умолчанию ru-RU)


class ProductReview(msgspec.Struct, forbid_unknown_fields=True, kw_only=True):
    id: int  # Идентификатор отзыва
    invoice_id: int  # Номер заказа
    owner_id: int  # Идентификатор торговой площадки
    type: str  # Тип отзыва: good или bad
    good: Optional[int] = None  # Идентификатор товара (если не был передан в запросе)
    name: Optional[str] = None  # Название товара (если не было передано в запросе)
    date: datetime  # Дата отзыва
    info: str  # Содержание отзыва
    comment: Optional[str] = None  # Комментарий продавца
    dateUtc: datetime


class ProductReviewsResponse(msgspec.Struct, forbid_unknown_fields=True, kw_only=True):
    retval: int  # Код выполнения запроса (0 - успех, 1 и другие - ограничения)
    retdesc: Optional[str] = None  # Описание кода выполнения запроса
    total_pages: Optional[int] = msgspec.field(name='totalPages', default=None)  # Всего страниц
    total_items: Optional[int] = msgspec.field(name='totalItems', default=None)  # Всего отзывов
    total_good: Optional[int] = msgspec.field(name='totalGood', default=None)  # Всего положительных отзывов
    total_bad: Optional[int] = msgspec.field(name='totalBad', default=None)  # Всего отрицательных отзывов
    reviews: List[ProductReview] = msgspec.field(name='review', default=None)  # Список отзывов


class OrderCol(StrEnum):
    NAME = "name"
    PRICE = "price"
    CNT_SELL = "cntsell"
    CNT_RETURN = "cntreturn"
    CNT_GOOD_RESPONSES = "cntgoodresponses"
    CNT_BAD_RESPONSES = "cntbadresponses"


class OrderDir(StrEnum):
    ASC = "asc"
    DESC = "desc"


class ShowHidden(IntEnum):
    WITHOUT_HIDDEN = 0  # Без скрытых товаров
    WITH_HIDDEN = 1  # Со скрытыми товарами
    ONLY_HIDDEN = 2  # Только скрытые товары


class LocaleSellerProducts(StrEnum):
    """Язык отображения информации."""
    RU_RU = "ru-RU"
    EN_US = "en-US"


class SellerProductsRequest(BaseStruct, forbid_unknown_fields=True):
    order_col: OrderCol = OrderCol.CNT_SELL  # Поле сортировки (по умолчанию - количество продаж)
    order_dir: OrderDir = OrderDir.DESC  # Порядок сортировки (по умолчанию - по убыванию)
    rows: Annotated[
        int,
        Meta(ge=10, le=1000)
    ] = 10  # Количество на странице (по умолчанию 10, не более 1000)
    page: Annotated[
        int,
        Meta(ge=1)
    ] = 1  # Номер страницы (по умолчанию 1)
    currency: Optional[Currency] = Currency.RUB  # Тип валюты для отображения цены товара
    lang: Optional[
        LocaleSellerProducts] = LocaleSellerProducts.RU_RU  # Язык отображения информации (по умолчанию ru-RU)
    show_hidden: Optional[
        ShowHidden] = ShowHidden.WITHOUT_HIDDEN  # Скрытые товары (0 - без скрытых, 1 - со скрытыми, 2 - только скрытые)
    owner_id: Optional[OwnerID] = msgspec.UNSET  # Идентификатор торговой площадки (опционально)


class ProductRow(msgspec.Struct, forbid_unknown_fields=True, kw_only=True):
    id_goods: int
    name_goods: str
    info_goods: Optional[str] = None
    add_info: Optional[str] = None
    price: float
    currency: Currency  # Сделать выдачу Currency
    cnt_sell: int
    cnt_sell_hidden: int
    cnt_return: int
    cnt_return_hidden: int
    cnt_goodresponses: int
    cnt_goodresponses_hidden: int
    cnt_badresponses: int
    cnt_badresponses_hidden: int
    price_usd: float
    price_rur: float
    price_eur: float
    price_uah: float
    in_stock: int
    num_in_stock: int
    visible: int
    commiss_agent: float
    has_discount: bool
    num_options: int
    sale_info: Optional[SaleInfo] = None
    owner_id: int
    release_date: Optional[datetime] = None
    num_in_stock: Optional[int] = None


class SellerProductsResponse(msgspec.Struct, forbid_unknown_fields=True, kw_only=True):
    retval: int
    retdesc: Optional[str] = None
    id_seller: Optional[int] = None
    name_seller: Optional[str] = None
    cnt_goods: Optional[int] = None
    pages: Optional[int] = None
    page: Optional[int] = None
    order_col: Optional[OrderCol] = None
    order_dir: Optional[OrderDir] = None
    rows: Optional[List[ProductRow]] = None
    rating_seller: Optional[float] = None
    show_hidden: Optional[float] = None


class CurrencyProductDiscount(StrEnum):
    RUB = "RUB"  # Российский рубль
    RUR = "RUR"  # Российский рубль

    USD = "USD"  # Доллар США
    EUR = "EUR"  # Евро
    UAH = "UAH"  # Украинская гривна
    MBTC = "mBTC"


class ProductDiscountRequest(msgspec.Struct, forbid_unknown_fields=True):
    product_id: int  # Идентификатор товара (целое число)
    currency: CurrencyProductDiscount  # Тип валюты (USD, RUR, EUR, UAH, mBTC)
    email: str  # Email покупателя


class ProductDiscountInfo(msgspec.Struct, forbid_unknown_fields=True):
    price: float  # Цена с учетом скидки
    currency: CurrencyProductDiscount  # Валюта товара


class DiscountInfo(msgspec.Struct, forbid_unknown_fields=True):
    percent: float  # Процент скидки
    total: float  # Общая сумма покупок (всегда в USD)
    currency: Literal['USD']  # Валюта скидки (всегда USD)


class ProductDiscountResponse(msgspec.Struct, forbid_unknown_fields=True):
    retval: int  # Код выполнения запроса (0 - успех)
    retdesc: Optional[str] = None  # Расшифровка кода выполнения запроса
    product: Optional[ProductDiscountInfo] = None  # Информация о товаре
    discount: Optional[DiscountInfo] = None  # Информация о скидке


class ProductSearchRequest(msgspec.Struct, forbid_unknown_fields=True):
    # Строка поиска
    search: Annotated[
        Optional[str],
        Meta(description="Строка поиска")
    ] = None
    currency: Annotated[
        Optional[Currency],
        Meta(description="Тип валюты для отображения стоимости товара: USD, RUB, EUR, UAH")
    ] = Currency.RUB
    # Номер страницы (по умолчанию 1)
    page: Annotated[
        int,
        Meta(
            ge=1,  # Минимальное значение 1
            description="Номер страницы (по умолчанию 1)"
        )
    ] = 1
    # Количество строк на странице (по умолчанию 20, максимум 500)
    rows: Annotated[
        int,
        Meta(
            ge=20,  # Минимальное значение 20
            le=500,  # Максимальное значение 500
            description="Количество строк на странице (по умолчанию 20, максимум 500)"
        )
    ] = 20

    # Язык отображения информации (по умолчанию ru-RU)
    lang: Annotated[
        Optional[Locale],
        Meta(description="Язык отображения информации (по умолчанию ru-RU)")
    ] = Locale.RU_RU


class Snippet(msgspec.Struct, forbid_unknown_fields=True):
    name: Optional[str] = None  # Название товара с найденной строкой поиска
    info: Optional[str] = None  # Фрагмент(ы) описания товара с найденной строкой поиска


class ProductSearchInfo(msgspec.Struct, forbid_unknown_fields=True):
    id: int  # Идентификатор товара
    name: str  # Название товара
    price: float  # Стоимость товара
    agency_fee: Optional[float] = None  # Партнерское вознаграждение %
    snippets: Optional[Snippet] = None  # Информация о товаре с найденной строкой поиска
    sale_info: Optional[SaleInfo] = None  # Информация о распродаже


class PageInfo(msgspec.Struct, forbid_unknown_fields=True):
    num: int  # Номер страницы, переданный в запросе
    rows: int  # Количество строк на странице
    cnt: int  # Количество страниц


class ProductSearchResponse(msgspec.Struct, forbid_unknown_fields=True):
    retval: int  # Код выполнения запроса (0 - успех)
    retdesc: Optional[str] = None  # Расшифровка кода выполнения запроса
    pages: Optional[PageInfo] = None  # Информация о страницах
    products: Optional[List[ProductSearchInfo]] = None  # Список продуктов
    search: Optional[str] = None  # Строка поиска, переданная в запросе
    currency: Optional[str] = None  # Тип валюты для отображения цены, переданный в запросе


class ProductImageRequest(BaseStruct, forbid_unknown_fields=True):
    # Идентификатор товара
    id_d: Annotated[
        int,
        Meta(description="Идентификатор товара (целое число)")
    ]

    # Максимальная длина в пикселях по бОльшей стороне
    maxlength: Annotated[
        Optional[int],
        Meta(description="Максимальная длина в пикселях по бОльшей стороне")
    ] = msgspec.UNSET

    # Максимальная ширина изображения
    w: Annotated[
        Optional[int],
        Meta(description="Максимальная ширина изображения (целое число)")
    ] = msgspec.UNSET

    # Максимальная высота изображения
    h: Annotated[
        Optional[int],
        Meta(description="Максимальная высота изображения (целое число)")
    ] = msgspec.UNSET

    # Обрезание для образования квадрата
    crop: Annotated[
        Optional[bool],
        Meta(description="Обрезание бОльших сторон прямоугольника для образования квадрата (true | false)")
    ] = msgspec.UNSET


class ProductImageResponse(msgspec.Struct, forbid_unknown_fields=True):
    image_data: Optional[bytes] = None  # Данные изображения в бинарном виде


class CloneProductRequest(BaseStruct, forbid_unknown_fields=True):
    product_id: int  # Идентификатор товара
    count: Annotated[int, Meta(ge=1, le=5)] = 1  # Количество создаваемых копий (по умолчанию: 1, не более 5)
    categories: Optional[bool] = False  # Разместить копии в тех же категориях (по умолчанию: false)
    notify: Optional[bool] = False  # Копировать настройки уведомлений (по умолчанию: false)
    discounts: Optional[bool] = False  # Копировать настройки скидок (по умолчанию: false)
    options: Optional[bool] = False  # Копировать настройки дополнительных параметров (по умолчанию: false)
    comissions: Optional[bool] = False  # Копировать настройки компенсаций (по умолчанию: false)
    gallery: Optional[bool] = False  # Копировать изображения и видео (по умолчанию: false)


class ErrorInfo(msgspec.Struct, forbid_unknown_fields=True):
    code: str  # Код ошибки
    message: str  # Описание кода выполнения


class Content(msgspec.Struct, forbid_unknown_fields=True):
    products: List[int]  # Идентификаторы созданных товаров


class CloneProductResponse(msgspec.Struct, forbid_unknown_fields=True):
    retval: int  # Код выполнения запроса (0 - успех, 1 - ошибка)
    retdesc: Optional[str] = None  # Описание кода выполнения
    errors: Optional[List[ErrorInfo]] = None  # Массив ошибок, если есть
    content: Optional[Content] = None  # Тело ответа (если успешно)


class SellerOfferProductsRequest(BaseStruct, forbid_unknown_fields=True):
    # Название товара (необязательное поле)
    productName: Annotated[
        Optional[str],
        Meta(description="Название товара (строка)")
    ] = msgspec.UNSET

    # Идентификатор товара (необязательное поле)
    productId: Annotated[
        Optional[int],
        Meta(description="Идентификатор товара (целое число)")
    ] = msgspec.UNSET

    # Только товары в наличии
    onlyInStock: Annotated[
        Optional[bool],
        Meta(description="Только товары в наличии (по умолчанию: false)")
    ] = False

    # Только с индивидуальными комиссионными
    onlyIndividual: Annotated[
        Optional[bool],
        Meta(description="Только с индивидуальными комиссионными (по умолчанию: false)")
    ] = False

    # Номер страницы
    page: Annotated[
        int,
        Meta(ge=1, description="Номер страницы (целое число)")
    ] = 1

    # Количество элементов на странице (1 - 100)
    count: Annotated[
        int,
        Meta(ge=1, le=100, description="Количество элементов на странице (целое число, 1 - 100)")
    ] = 20


class ProductName(msgspec.Struct, forbid_unknown_fields=True):
    locale: str  # Локаль (например, 'ru-RU' или 'en-US')
    value: str  # Название товара на указанной локали


class ProductItem(msgspec.Struct, forbid_unknown_fields=True):
    product_id: int  # Идентификатор товара
    name: List[ProductName]  # Название товара
    price: float  # Цена
    currency: Currency  # Валюта (RUB, USD, UAH, EUR)
    in_affiliate: bool  # Товар участвует в партнерской программе
    individual_percent: int  # Индивидуальный процент отчислений
    global_percent: int  # Процент отчислений в настройках товара
    last_change: Optional[str] = None  # Последние изменения (ISO 8601)


class ContentInfo(msgspec.Struct, forbid_unknown_fields=True):
    page: int  # Номер страницы
    count: int  # Количество на странице
    total_count: int  # Количество всех элементов
    total_pages: int  # Всего страниц
    has_next_page: bool  # Признак наличия следующей страницы
    has_previous_page: bool  # Признак наличия предыдущей страницы
    items: List[ProductItem]  # Список товаров


class SellerOfferProductsResponse(msgspec.Struct, forbid_unknown_fields=True):
    retval: int  # Код выполнения запроса (0 - успех, 1 - ошибка)
    retdesc: Optional[str] = None  # Описание кода выполнения запроса
    errors: Optional[List[ErrorInfo]] = None  # Массив ошибок (если есть)
    content: Optional[ContentInfo] = None  # Тело ответа (если нет ошибок)
