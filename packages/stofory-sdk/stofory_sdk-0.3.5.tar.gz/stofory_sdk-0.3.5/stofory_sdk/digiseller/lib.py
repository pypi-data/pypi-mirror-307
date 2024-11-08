from abc import ABC, abstractmethod
from typing import Any

import msgspec


class BaseCustomSchemaType(ABC):

    @abstractmethod
    def _validate(self):
        pass

    @abstractmethod
    def into_encoding_type(self) -> Any:
        pass

    @abstractmethod
    def into_decoding_type(self) -> Any:
        pass

    @abstractmethod
    def value(self) -> Any:
        pass

    @classmethod
    @abstractmethod
    def from_inner_type(cls, value: Any) -> Any:
        pass

    def __repr__(self):
        return str(self.value())


class BaseStruct(msgspec.Struct):
    def to_dict(self, exclude: list[str] = None) -> dict[str, Any]:
        exclude = exclude or []

        result_dict = {f: getattr(self, f) for f in self.__struct_fields__ if
                f not in exclude and getattr(self, f, None) != msgspec.UNSET}

        for k, v in result_dict.items():
            if isinstance(v, BaseCustomSchemaType):
                result_dict[k] = v.into_encoding_type()

        return result_dict