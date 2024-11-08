from datetime import datetime
from enum import StrEnum
from typing import Annotated, Any, Optional, List

from msgspec import Meta

from ..lib import BaseStruct
from ..schemas import CurrencyDigiseller

__all__ = ('CaptchaResponse', 'PartnerRegistrationRequest', 'PartnerRegistrationResponse', 'PermissionsResponse',
           'PaymentVerificationResponse', 'SaleInfoResponse', 'UniqueCodeState', 'BuyerInfo', 'Content')


class CaptchaResponse(BaseStruct, forbid_unknown_fields=True):
    retval: int  # код выполнения запроса
    retdesc: Optional[str]  # описание ошибки (если retval != 0)
    id_seller: Optional[int] = None  # идентификатор продавца
    id_request: Optional[int] = None  # номер запроса для следующего шага
    img_url: Optional[str] = None  # URL изображения капчи


class PartnerRegistrationRequest(BaseStruct, forbid_unknown_fields=True):
    id_seller: Annotated[int, Meta(gt=0)]  # Идентификатор продавца
    id_request: int  # Номер запроса, полученный в предыдущем шаге
    turing_num: int  # Введенное партнером проверочное число (капча)
    r_email: str  # Email пользователя (партнера)
    r_redirect_url: str  # URL для перенаправления


class PartnerRegistrationResponse(BaseStruct, forbid_unknown_fields=True):
    retval: int  # Код выполнения запроса
    retdesc: str  # Текст ошибки при retval != 0
    id_agent: Optional[int] = None  # ID агента (0, если регистрация еще не завершена)


class PermissionsResponse(BaseStruct, forbid_unknown_fields=True):
    description_create: bool = False
    description_edit: bool = False
    description_view: bool = False
    content_upload: bool = False
    content_change: bool = False
    content_delete: bool = False
    gallery_add: bool = False
    gallery_change: bool = False
    option_read: bool = False
    option_add: bool = False
    option_edit: bool = False
    option_delete: bool = False
    view_operations: bool = False
    view_invoice: bool = False
    sales_statistics_view: bool = False
    agent_sales_statistics_view: bool = False
    view_personal_offer: bool = False
    read_commission_template: bool = False
    create_commission_template: bool = False
    edit_commission_template: bool = False
    delete_commission_template: bool = False
    apply_commission_template: bool = False
    debates_read: bool = False
    debates_write: bool = False
    debates_delete: bool = False
    token_get_perms: bool = False


class UniqueCodeState(BaseStruct, forbid_unknown_fields=True):
    state: int
    options: Any = None  # Кто ты воин?
    date_check: Optional[datetime] = None  # строка. необязательное поле
    date_delivery: Optional[datetime] = None  # строка. необязательное поле
    date_refuted: Optional[datetime] = None  # строка. необязательное поле
    date_confirmed: Optional[datetime] = None  # строка. необязательное поле


class PaymentVerificationOption(BaseStruct, forbid_unknown_fields=True):
    id: int  # атрибут id - уникальный идентификатор параметра (кого хуя они option пишут)
    name: str
    value: str
    variant_id: Optional[int] = None  # целое число. может быть пустым (только для полей 'radio' и 'select')


class PaymentVerificationResponse(BaseStruct, kw_only=True, forbid_unknown_fields=True):
    retval: int
    retdesc: Optional[str]
    inv: int
    id_goods: int
    amount: float
    type_curr: CurrencyDigiseller
    amount_usd: float

    profit: Optional[float] = None  # Так как в одном из примеров profit пустое значение
    date_pay: Optional[datetime] = None
    email: Optional[str]
    method: Optional[str] = None  # Ебать его не было в документации - КЛЯНУСЬ НЕ БЫЛО. Видимо метод оплаты
    name_invoice: Optional[str]
    lang: Optional[str]

    agent_id: int
    agent_percent: float
    query_string: Optional[str]  # base64-закодированная строка

    unit_goods: Optional[int] = None  # только для товаров с нефиксированной ценой
    cnt_goods: Optional[float] = None  # только для товаров с нефиксированной ценой
    promo_code: Optional[str] = None  # только если при оплате был использован промо-код
    bonus_code: Optional[str] = None  # только если после оплате был выдан промо-код
    cart_uid: Optional[str] = None  # только если товар был добавлен и оплачен через корзину

    unique_code_state: Optional[
        UniqueCodeState] = None  # необязательное поле уникальный код (состояние и даты проверки)
    options: Optional[List[PaymentVerificationOption]] = None  # только для товаров с доп. параметрами


# Модель для поля feedback
class UserFeedback(StrEnum):
    POSITIVE = 'positive'
    NEGATIVE = 'negative'


class Feedback(BaseStruct, forbid_unknown_fields=True):
    deleted: bool
    feedback: str
    feedback_type: UserFeedback
    comment: str


# Модель для информации о покупателе
class BuyerInfo(BaseStruct, kw_only=True, forbid_unknown_fields=True):
    payment_method: str
    payment_aggregator: str
    account: Optional[str] = None
    email: str
    phone: Optional[str] = None
    skype: Optional[str] = None
    whatsapp: Optional[str] = None
    ip_address: Optional[str]


class ContentOption(BaseStruct, forbid_unknown_fields=True):
    id: int  # атрибут id - уникальный идентификатор параметра
    name: str
    user_data: str
    user_data_id: Optional[int] = None  # целое число. может быть пустым (только для полей 'radio' и 'select')


class PaymentHoldState(StrEnum):
    FREE = 'free'
    LOCKED = 'locked'
    EMPTY = ''


# Основная модель content
class Content(BaseStruct, forbid_unknown_fields=True, kw_only=True):
    item_id: int
    cart_uid: Optional[str] = None  # только если товар был добавлен и оплачен через корзину
    name: Optional[str]
    amount: float  # сумма, зачисленная на ваш счет обязательно проверяйте данное значение!
    currency_type: CurrencyDigiseller
    invoice_state: int

    purchase_date: datetime
    date_pay: Optional[datetime] = None  # строка. необязательное поле

    agent_id: Optional[int] = None  # ID партнера, если продажа была совершена с участием партнера
    agent_percent: Optional[float] = None  # процент партнерского вознаграждения
    query_string: Optional[str]  # # base64-закодированная строка,

    unit_goods: Optional[int] = None  # только для товаров с нефиксированной ценой
    cnt_goods: Optional[float] = None  # только для товаров с нефиксированной ценой
    promo_code: Optional[str] = None  # только если при оплате был использован промо-код
    bonus_code: Optional[str] = None  # только если после оплате был выдан промо-код

    feedback: Optional[Feedback] = None  # отзыв покупателя
    unique_code_state: Optional[
        UniqueCodeState] = None  # необязательное поле уникальный код (состояние и даты проверки)
    options: Optional[List[ContentOption]] = None
    buyer_info: BuyerInfo
    referer: Optional[str] = None  # Ебать его не было в документации - КЛЯНУСЬ НЕ БЫЛО.
    owner: int
    day_lock: int
    lock_state: Optional[PaymentHoldState]
    profit: Optional[float] = None  # Зачислено на счёт
    agent_fee: Optional[float] = None  # Коммисия агента


class Error(BaseStruct, forbid_unknown_fields=True):
    code: str
    message: str


# Модель для ответа SaleInfoResponse
class SaleInfoResponse(BaseStruct, forbid_unknown_fields=True):
    retval: int
    retdesc: Optional[str]
    errors: Optional[List[Error]]
    content: Optional[Content]
