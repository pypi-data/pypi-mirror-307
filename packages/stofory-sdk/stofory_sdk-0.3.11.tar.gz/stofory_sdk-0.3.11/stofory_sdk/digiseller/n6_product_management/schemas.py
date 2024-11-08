import enum
from datetime import datetime

import msgspec

from ..schemas import Locale, Currency, BaseResponse, VariantTypes


class AsyncTaskStatuses(enum.IntEnum):
    PENDING = 0
    IN_PROGRESS = 1
    FAILED = 2
    COMPLETED = 3


class ProductStatuses(enum.StrEnum):
    DISABLED = "disabled"
    ENABLED = "enabled"


class GalleryTypes(enum.StrEnum):
    IMAGE = "image"
    VIDEO = "video"


class ProductFixedTypes(enum.StrEnum):
    TEXT = "text"
    DIGISELLERCODE = "digisellercode"
    FILE = "file"


class ProductUnfixedTypes(enum.StrEnum):
    DIGISELLERCODE = "digisellercode"


class ProductName(msgspec.Struct, forbid_unknown_fields=True):
    locale: Locale
    value: str


class ProductDescription(msgspec.Struct, forbid_unknown_fields=True):
    locale: Locale
    value: str


class ProductAddInfo(msgspec.Struct, forbid_unknown_fields=True):
    locale: Locale
    value: str


class ProductFixedPrice(msgspec.Struct, forbid_unknown_fields=True):
    price: int
    currency: Currency


class ProductUnfixedPrice(msgspec.Struct, forbid_unknown_fields=True):
    price: float
    currency: Currency
    unit_quantity: int
    unit_name: str


class CategoryOwners(enum.IntEnum):
    OWN_SHOP = 0  # собственный магазин
    PLATI_MARKET = 1  # plati.market
    WMCENTER = 2  # wmcenter.net
    GGSELL = 3  # ggsel


class Platforms(enum.StrEnum):
    PLATI = 'plati'
    WMCENTER = 'wmcenter'
    GGSELL = 'ggsel'


class ProductCategory(msgspec.Struct, forbid_unknown_fields=True):
    owner: CategoryOwners
    category_id: int


class ProductBonus(msgspec.Struct, forbid_unknown_fields=True):
    enabled: bool
    percent: int


class ProductGuarantee(msgspec.Struct, forbid_unknown_fields=True):
    enabled: bool
    value: int


class ProductVerifyCode(msgspec.Struct, forbid_unknown_fields=True):
    auto_verify: bool
    verify_url: str


class ProductPreorder(msgspec.Struct, forbid_unknown_fields=True):
    enabled: bool
    delivery_date: datetime


class InstructionTypes(enum.StrEnum):
    TEXT = "text"
    URL = "url"


class InstructionLocale(msgspec.Struct, forbid_unknown_fields=True):
    locale: Locale
    value: str


class ProductInstruction(msgspec.Struct, forbid_unknown_fields=True):
    type: InstructionTypes
    locales: list[InstructionLocale]


class SalesLimits(enum.IntEnum):
    HIDDEN = -1
    ONE = 1
    TEN = 10
    FIFTY = 50
    HUNDRED = 100
    THOUSAND = 1000


class OnlineCheckoutCategory(enum.StrEnum):
    GOODS = "Goods"  # товар
    EXERCISE_GOODS = "ExciseGoods"  # подакцизный товар
    WORK = "Work"   # работа
    SERVICE = "Service"  # услуга
    GAMBLING_BET = "GamblingBet"    # ставка в азартной игре
    GAMBLING_PRICE = "GamblingPrize"    # выигрыш в азартной игре
    LOTTERY_TICKET = "LotteryTicket"    # лотерейный билет
    LOTTERY_PRIZE = "LotteryPrize"  # выигрыш в лотерею
    INTELLECTUAL_PROPERTY_GRANT = "IntellectualPropertyGrant"   # предоставление РИД
    PAYMENT = "Payment"  # платеж
    AGENCY_FEE = "AgencyFee"    # агентское вознаграждение
    COMPOSITE_SUBJECT = "CompositeSubject"  # составной предмет расчета
    OTHER_SUBJECT = "OtherSubject"  # иной предмет расчета
    PROPERTY_RIGHT = "PropertyRight"  # имущественное право
    NON_OPERATING_INCOME = "NonOperatingIncome"  # внереализационный доход
    INSURANCE_PREMIUMS = "InsurancePremiums"  # страховой сбор
    TRADE_FEE = "TradeFee"  # торговый сбор
    RESORT_FEE = "ResortFee"   # курортный сбор
    PLEDGE = "Pledge"  # залог


class OnlineCheckoutTax(enum.StrEnum):
    VAT20 = "vat20"  # - расчетная ставка 20 %
    VAT10 = "vat10"  # - расчетная ставка 10 %
    VAT110 = "vat110"  # - расчетная ставка 10 / 110
    VAT120 = "vat120"  # - расчетная ставка 20 / 120
    VAT0 = "vat0"  # - расчетная ставка 0 %
    NO_VAT = "no_vat"  # - НДС не накладывается


class LimitationTypes(enum.StrEnum):
    NONE = "None"
    MIN_AND_MAX = "MinAndMax"
    FIXED_QUANTITY = "FixedQuantity"


class ProductUnfixedLimitation(msgspec.Struct, forbid_unknown_fields=True):
    type: LimitationTypes
    only_integer: bool
    limitations: list[int | float]


class ProductUnfixedDiscount(msgspec.Struct, forbid_unknown_fields=True):
    unit_for_discount: float
    discount: int


class CategoryName(msgspec.Struct, forbid_unknown_fields=True):
    locale: Locale
    value: str | None


class PlatformCategory(msgspec.Struct, forbid_unknown_fields=True):
    id: int
    level: int
    parent_id: int
    name: list[CategoryName]
    can_add: bool
    children: list["PlatformCategory"] | None = None


class PlatformSubcategory(msgspec.Struct, forbid_unknown_fields=True):
    id: int
    title: str
    name: list[CategoryName]


class VariantPriceUpdate(msgspec.Struct, forbid_unknown_fields=True):
    variant_id: int
    rate: float
    type: VariantTypes | None = None


class ProductIdResult(msgspec.Struct, forbid_unknown_fields=True):
    product_id: int


class StatusResult(msgspec.Struct, forbid_unknown_fields=True):
    status: str


class UploadImageResult(msgspec.Struct, forbid_unknown_fields=True):
    preview_id: int
    filename: str


class AddVideoResult(msgspec.Struct, forbid_unknown_fields=True):
    preview_id: int
    url: str


class AsyncTaskError(msgspec.Struct, forbid_unknown_fields=True):
    key: str = msgspec.field(name="Key")
    value: str = msgspec.field(name="Value")


"""

The following classes are used to validate the input and output data of the API endpoints.

"""


class CreateUniquefixedRequest(msgspec.Struct, forbid_unknown_fields=True):
    content_type: ProductFixedTypes
    name: list[ProductName]
    price: ProductFixedPrice
    categories: list[ProductCategory]
    description: list[ProductDescription]
    address_required: bool

    bonus: ProductBonus | None = None
    guarantee: ProductGuarantee | None = None
    add_info: list[ProductAddInfo] | None = None
    comission_partner: int | None = None
    trial_url: str | None = None
    preorder: ProductPreorder | None = None
    verify_code: ProductVerifyCode | None = None
    present_product_id: int | None = None
    sales_limit: SalesLimits | None = None
    online_checkout_name: str | None = None
    online_checkout_category: OnlineCheckoutCategory | None = None
    online_checkout_tax: OnlineCheckoutTax | None = None


class CreateUniquefixedResponse(BaseResponse, forbid_unknown_fields=True):
    content: ProductIdResult | None


class CreateUniqueunfixedRequest(msgspec.Struct, forbid_unknown_fields=True):
    content_type: ProductFixedTypes
    name: list[ProductName]
    prices: ProductUnfixedPrice
    categories: list[ProductCategory]
    description: list[ProductDescription]
    address_required: bool
    limitations: ProductUnfixedLimitation

    bonus: ProductBonus | None = None
    guarantee: ProductGuarantee | None = None
    add_info: list[ProductAddInfo] | None = None
    comission_partner: int | None = None
    discounts: list[ProductUnfixedDiscount] | None = None
    instruction: ProductInstruction | None = None
    present_product_id: int | None = None
    sales_limit: SalesLimits | None = None
    online_checkout_name: str | None = None
    online_checkout_category: OnlineCheckoutCategory | None = None
    online_checkout_tax: OnlineCheckoutTax | None = None


class CreateUniqueunfixedResponse(BaseResponse, forbid_unknown_fields=True):
    content: ProductIdResult | None


class UpdateUniquefixedRequest(CreateUniquefixedRequest, forbid_unknown_fields=True, kw_only=True):
    enabled: bool


class UpdateUniquefixedResponse(BaseResponse, forbid_unknown_fields=True):
    content: StatusResult | None


class UpdateUniqueunfixedRequest(CreateUniqueunfixedRequest, forbid_unknown_fields=True, kw_only=True):
    enabled: bool


class UpdateUniqueunfixedResponse(BaseResponse, forbid_unknown_fields=True):
    content: StatusResult | None


class UploadImagesResponse(BaseResponse, forbid_unknown_fields=True):
    content: list[UploadImageResult] | None


class AddVideosRequest(msgspec.Struct, forbid_unknown_fields=True):
    urls: list[str]


class AddVideosResponse(BaseResponse, forbid_unknown_fields=True):
    content: list[AddVideoResult] | None


class EditGalleryRequest(msgspec.Struct, forbid_unknown_fields=True):
    enabled: bool | None = None
    index: int | None = None
    delete: bool | None = None


# # хз шо тут делать пока, крашит базовый сервис
# class EditGalleryResponse(BaseResponse, forbid_unknown_fields=True):
#     # content: StatusResult | None
#     pass


class UpdateStatusMassRequest(msgspec.Struct, forbid_unknown_fields=True):
    new_status: ProductStatuses
    products: list[int]


class UpdateStatusMassResponse(BaseResponse, forbid_unknown_fields=True):
    content: str | None


class UpdatePriceMassRequestItem(msgspec.Struct, forbid_unknown_fields=True):
    product_id: int
    price: float
    variants: list[VariantPriceUpdate] | None = None


class UpdatePriceMassRequest(msgspec.Struct, forbid_unknown_fields=True):
    items: list[UpdatePriceMassRequestItem]


class UpdatePriceMassResponse(BaseResponse, forbid_unknown_fields=True):
    content: str | None


class AddProductToCategoryResponse(BaseResponse, forbid_unknown_fields=True):
    content: StatusResult | None


class PlatformCategoriesResponse(BaseResponse, forbid_unknown_fields=True):
    content: list[PlatformCategory] | None


class PlatformSubcategoriesResponse(BaseResponse, forbid_unknown_fields=True):
    content: list[PlatformSubcategory] | None


class AsyncTaskStatusResponse(msgspec.Struct, forbid_unknown_fields=True):
    task_id: str = msgspec.field(name="TaskId")
    status: AsyncTaskStatuses = msgspec.field(name="Status")
    success_count: int = msgspec.field(name="SuccessCount")
    error_count: int = msgspec.field(name="ErrorCount")
    total_count: int = msgspec.field(name="TotalCount")
    errors_descriptions: list[AsyncTaskError] | None = msgspec.field(name="ErrorsDescriptions")
