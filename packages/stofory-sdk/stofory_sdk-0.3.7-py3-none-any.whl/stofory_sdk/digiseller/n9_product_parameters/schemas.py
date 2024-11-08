import msgspec

from ..schemas import Locale, BaseResponse, VariantTypes, OptionTypes


class OptionName(msgspec.Struct, forbid_unknown_fields=True):
    locale: Locale
    value: str


class OptionComment(msgspec.Struct, forbid_unknown_fields=True):
    locale: Locale
    value: str


class Option(msgspec.Struct, forbid_unknown_fields=True):
    id: int
    type: OptionTypes
    order: int
    name: list[OptionName] | None
    comment: list[OptionComment] | None

    separate_content: int | None   # to bool, лишняя хня
    modifier_visible: int | None   # to bool, лишняя хня


class VariantName(msgspec.Struct, forbid_unknown_fields=True):
    locale: Locale
    value: str


class Variant(msgspec.Struct, forbid_unknown_fields=True):
    variant_id: int
    name: list[VariantName] | None
    type: VariantTypes
    rate: float
    is_default: bool
    visible: bool
    order: int


class VariantCreateRequest(msgspec.Struct, forbid_unknown_fields=True):
    name: list[VariantName]
    type: VariantTypes
    rate: int
    default: bool
    order: int


class VariantCreateResponse(msgspec.Struct, forbid_unknown_fields=True):
    variants: list[int]


class OptionDetails(msgspec.Struct, forbid_unknown_fields=True):
    id: int
    type: OptionTypes
    name: list[OptionName] | None
    comment: list[OptionComment] | None
    order: int
    no_default: bool
    separate_content: bool
    required: bool
    modifier_visible: bool
    variants: list[Variant] | None


class OptionCreateResponse(msgspec.Struct, forbid_unknown_fields=True):
    option_id: int

    parameter_id: int | None    # лишняя хня с тем же значением что и в option_id


class UpdateDeleteResponse(msgspec.Struct, forbid_unknown_fields=True):
    status: str


class ProductParametersResponse(BaseResponse, forbid_unknown_fields=True):
    content: list[Option] | None


class ProductParameterResponse(BaseResponse, forbid_unknown_fields=True):
    content: OptionDetails | None


class ProductParameterCreateRequest(msgspec.Struct, forbid_unknown_fields=True):
    product_id: int
    name: list[OptionName] | None
    comment: list[OptionComment] | None
    type: OptionTypes
    separate_content: bool
    required: bool
    modifier_visible: bool
    order: int
    variants: list[VariantCreateRequest] | None


class ProductParameterCreateResponse(BaseResponse, forbid_unknown_fields=True):
    content: OptionCreateResponse | None


class ProductParameterUpdateRequest(msgspec.Struct, forbid_unknown_fields=True):
    option_id: int
    name: list[OptionName] | None
    comment: list[OptionComment] | None
    type: OptionTypes
    separate_content: bool
    required: bool
    modifier_visible: bool
    order: int


class ProductParameterUpdateResponse(BaseResponse, forbid_unknown_fields=True):
    content: UpdateDeleteResponse | None


class ProductParameterDeleteResponse(BaseResponse, forbid_unknown_fields=True):
    content: UpdateDeleteResponse | None


class ProductParameterVariantCreateRequest(msgspec.Struct, forbid_unknown_fields=True):
    variants: list[VariantCreateRequest]


class ProductParameterVariantCreateResponse(BaseResponse, forbid_unknown_fields=True):
    content: VariantCreateResponse | None


class ProductParameterVariantUpdateRequest(msgspec.Struct, forbid_unknown_fields=True):
    name: list[VariantName] | None
    type: VariantTypes
    rate: int
    default: bool
    visible: bool
    order: int


class ProductParameterVariantUpdateResponse(BaseResponse, forbid_unknown_fields=True):
    content: UpdateDeleteResponse | None


class ProductParameterVariantDeleteResponse(BaseResponse, forbid_unknown_fields=True):
    content: UpdateDeleteResponse | None
