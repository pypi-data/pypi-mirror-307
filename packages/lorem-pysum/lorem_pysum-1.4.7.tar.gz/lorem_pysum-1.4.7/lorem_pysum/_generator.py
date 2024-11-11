"""Generate random instances of the given Pydantic model type."""

from __future__ import annotations

from pathlib import Path

__all__ = ("generate",)

import dataclasses
import datetime
import importlib
import math
import typing
import uuid
from _decimal import Decimal
from copy import copy
from enum import Enum
from numbers import Number
from typing import Any, Optional, Type, TypeVar, Union
from uuid import UUID, uuid4

import annotated_types
from pydantic import (
    AnyHttpUrl,
    AnyUrl,
    AwareDatetime,
    BaseModel,
    DirectoryPath,
    EmailStr,
    FilePath,
    FutureDate,
    FutureDatetime,
    HttpUrl,
    IPvAnyAddress,
    IPvAnyInterface,
    IPvAnyNetwork,
    Json,
    NaiveDatetime,
    NameEmail,
    NewPath,
    PastDate,
    PastDatetime,
    SecretBytes,
    SecretStr,
    StringConstraints,
)
from pydantic.fields import FieldInfo
from pydantic.types import PaymentCardBrand as OriginalPaymentCardBrand
from pydantic_core import MultiHostUrl, PydanticUndefined, Url

extras_package_name = "pydantic_extra_types"
try:
    package = importlib.import_module(extras_package_name)
    color_package = importlib.import_module(f"{extras_package_name}.color")
    payment_package = importlib.import_module(f"{extras_package_name}.payment")
    routing_package = importlib.import_module(f"{extras_package_name}.routing_number")
    Color = color_package.Color
    PaymentCardBrand = payment_package.PaymentCardBrand
    PaymentCardNumber = payment_package.PaymentCardNumber
    ABARoutingNumber = routing_package.ABARoutingNumber
except ImportError:
    Color = str
    PaymentCardBrand = str
    PaymentCardNumber = str
    ABARoutingNumber = str
try:
    phone_package = importlib.import_module(f"{extras_package_name}.phone_numbers")
    PhoneNumber = phone_package.PhoneNumber
except ImportError:
    PhoneNumber = str

NoneType = type(None)
ModelType = TypeVar("ModelType", bound=BaseModel)
AnyNumber = Union[Number, float]
default_max_len = 1
default_date = datetime.date(year=1788, month=6, day=21)
default_time_delta = datetime.timedelta()
default_time = datetime.time()


@dataclasses.dataclass
class Metadata:
    """Filed info metadata."""

    gt: Optional[int] = None
    ge: Optional[int] = None
    lt: Optional[int] = None
    le: Optional[int] = None
    multiple_of: Optional[float] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    str_constraints: Optional[StringConstraints] = None


def generate(
    model_type: Type[ModelType],
    *_args: Any,
    use_default_values: bool = True,
    optionals_use_none: bool = False,
    overrides: Optional[dict[str, Any]] = None,
    explicit_default: bool = False,
) -> ModelType:
    """Generate an instance of a Pydantic model with random values.

    Any values provided in `kwargs` will be used as model field values
    instead of randomly generating them.

    :param model_type: Model type to generate an instance of.
    :param use_default_values: Whether to use model default values for
        non-None defaults.
    :param optionals_use_none: How to handle optional fields.
    :param overrides: Attributes to manually set on the model instance.
    :param explicit_default: Explicitly set fields to their default
        value, this means default values will be included in
        `model_dump(exclude+unset=True)`.
    :return: A randomly generated instance of the provided model type.
    """
    return _Generator(
        model_type,
        use_default_values=use_default_values,
        explicit_default=explicit_default,
        optionals_use_none=optionals_use_none,
        overrides=overrides,
    ).generate(model_type)


class _Generator:
    """Class to generate values for a model.

    Use of class here simplifies the function definitions and calls of
    the numerous recursive functions that were previously obligated to
    pass and accept as arguments, the same flags that can be held at a
    class level.
    """

    def __init__(  # noqa: PLR0913
        self,
        model_type: Type[ModelType],
        *,
        use_default_values: bool,
        optionals_use_none: bool,
        explicit_default: bool,
        overrides: Optional[dict[str, Any]],
    ) -> None:
        self.model_type = model_type
        self.use_default_values = use_default_values
        self.explicit_default = explicit_default
        self.optionals_use_none = optionals_use_none
        self.overrides = overrides or {}

    def generate(
        self,
        model_type: Type[ModelType],
        processed_models: Optional[list[Type[ModelType]]] = None,
    ) -> ModelType:
        """Generate an instance of the given model.

        :param model_type: Model type to generate instance of.
        :param processed_models: Models already processed, used for
            recursive calls to prevent infinite recursion.
        :return: Instance of model with fields populated.
        """
        # Copy prevents us from mutating original, if we mutated
        # original, sibling fields could be mistaken as recursive.
        processed_models = copy(processed_models) if processed_models else []
        processed_models.append(model_type)

        fields = {}
        for field_name, field_info in model_type.model_fields.items():
            if model_type == self.model_type and field_name in self.overrides:
                continue
            _get_metadata(field_info)

            # Handle default values for field.
            # noinspection PyDeprecation,Pydantic
            if (
                (field_info.default is not PydanticUndefined)
                or field_info.default_factory is not None
            ) and self.use_default_values:
                if not self.explicit_default:
                    continue
                if field_info.default is not PydanticUndefined:
                    fields[field_name] = field_info.default
                elif field_info.default_factory:
                    fields[field_name] = field_info.default_factory()
                continue

            # Generate value for this field.
            fields[field_name] = self._get_value(
                field_info.annotation or str, field_info, processed_models
            )

        if model_type == self.model_type:
            fields: dict[str, Any] = {**fields, **self.overrides}
        return model_type.model_construct(**fields)

    def _get_value(  # noqa: PLR0911,PLR0912,PLR0915
        self,
        type_: Any,
        field_info: FieldInfo,
        processed_models: list[Type[ModelType]],
        *,
        hashable: bool = False,
    ) -> Any:
        """Get a value of the given type."""
        metadata = _get_metadata(field_info)
        origin = typing.get_origin(type_)

        if self.optionals_use_none and NoneType in typing.get_args(type_):
            return None

        if origin is typing.Literal:
            return typing.get_args(type_)[0]

        # Generate collection of the collection type.
        # If type is dict create dict with proper key and value types.
        if origin is dict:
            k_type, v_type = typing.get_args(type_)
            return {
                self._get_value(
                    k_type, field_info, processed_models, hashable=True
                ): self._get_value(v_type, field_info, processed_models)
                for _ in range(default_max_len)
                if k_type not in processed_models and v_type not in processed_models
            }
        # List
        if origin is list:
            return self._get_list_values(
                type_, field_info, metadata.min_length, processed_models
            )
        if origin is None and type_ is list:
            return self._get_list_values(
                list[Any], field_info, metadata.min_length, processed_models
            )
        # Set
        if origin is set:
            return set(
                self._get_list_values(
                    type_,
                    field_info,
                    metadata.min_length,
                    processed_models,
                    hashable=True,
                )
            )
        if origin is None and type_ is set:
            return set(
                self._get_list_values(
                    set[Any],
                    field_info,
                    metadata.min_length,
                    processed_models,
                    hashable=True,
                )
            )
        # Tuple
        if origin is tuple:
            return tuple(
                self._get_value(arg, field_info, processed_models)
                for arg in typing.get_args(type_)
            )
        if origin is None and type_ is tuple:
            return tuple(
                self._get_list_values(
                    tuple[Any], field_info, metadata.min_length, processed_models
                )
            )

        # If union, pick among possible types avoiding NoneType.
        if _is_union(origin):
            type_choices = [
                arg_type
                for arg_type in typing.get_args(type_)
                if arg_type is not NoneType and arg_type not in processed_models
            ]
            # Only options are `None` or infinite recursion, use `None`.
            if not type_choices:
                return None
            return self._get_value(type_choices[0], field_info, processed_models)

        # Trivial to produce values.
        if type_ in [bytes, SecretBytes]:
            return bytes(1)
        if type_ in [str, SecretStr]:
            return _get_str_value(metadata)
        if type_ in [int, float]:
            return type_(_get_number_value(metadata))
        if type_ is Decimal:
            return Decimal(f"{_get_number_value(metadata)}")
        if type_ is bool:
            return True
        if type_ is Any:
            return {} if not hashable else "any"
        if type_ == datetime.date:
            return default_date
        if type_ == datetime.time:
            return default_time
        if type_ == datetime.timedelta:
            return default_time_delta
        if type_ == datetime.datetime:
            return datetime.datetime.fromordinal(default_date.toordinal())

        # Special Types.
        if type_ == UUID:
            if field_info.metadata and hasattr(field_info.metadata[0], "uuid_version"):
                if field_info.metadata[0].uuid_version == 1:
                    return uuid.uuid1()
                if field_info.metadata[0].uuid_version == 3:  # noqa: PLR2004
                    return uuid.uuid3(name="name", namespace=uuid4())
                if field_info.metadata[0].uuid_version == 4:  # noqa: PLR2004
                    return uuid.uuid4()
                if field_info.metadata[0].uuid_version == 5:  # noqa: PLR2004
                    return uuid.uuid5(name="name", namespace=uuid4())
            return uuid.uuid4()
        if type_ == Json:
            return '{"key": "value"}'
        if type_ == PastDate:
            return default_date
        if type_ == FutureDate:
            return datetime.date.today() + datetime.timedelta(days=1)
        if type_ == AwareDatetime:
            return datetime.datetime.fromordinal(default_date.toordinal()).astimezone(
                datetime.timezone.utc
            )
        if type_ in [NaiveDatetime, PastDatetime]:
            return datetime.datetime.fromordinal(default_date.toordinal())
        if type_ == FutureDatetime:
            return datetime.datetime.now() + datetime.timedelta(days=1)

        # Network Types
        if field_info.metadata and hasattr(field_info.metadata[0], "allowed_schemes"):
            schemes = field_info.metadata[0].allowed_schemes
            if "postgres" in schemes:
                return MultiHostUrl(
                    "postgresql://user:password@localhost:5432/database"
                )
            if "cockroachdb" in schemes:
                return Url("cockroachdb://user:password@localhost:26257/database")
            if "amqp" in schemes:
                return Url("amqp://user:password@localhost:5672/vhost")
            if "redis" in schemes:
                return Url("redis://localhost:6379")
            if "mongodb" in schemes:
                return MultiHostUrl("mongodb://user:password@localhost:27017/database")
            if "kafka" in schemes:
                return Url("kafka://localhost:9092")
            if "mysql" in schemes:
                return Url("mysql://user:password@localhost:3306/database")
            if "mariadb" in schemes:
                return Url("mariadb://user:password@localhost:3306/database")
            if "file" in schemes:
                return Url("file:///lorem/ipsum")
        if type_ in [AnyUrl, AnyHttpUrl, HttpUrl]:
            return Url("https://website.test")
        if type_ == EmailStr:
            return "email@website.example"
        if type_ == NameEmail:
            return "First Last <email@website.example>"
        if type_ == IPvAnyAddress:
            return "127.0.0.1"
        if type_ == IPvAnyInterface:
            return "0.0.0.0/0"
        if type_ == IPvAnyNetwork:
            return "192.168.1.0/24"
        if type_ in [FilePath, DirectoryPath, NewPath, Path]:
            return "/lorem/ipsum"

        # Extra Types
        if type_ == Color:
            return "#000"
        if type_ in [PaymentCardBrand, OriginalPaymentCardBrand]:
            return "Visa"
        if type_ == PaymentCardNumber:
            return "4111111111111111"
        if type_ == PhoneNumber:
            return "+1 (555) 555-5555"
        if type_ == ABARoutingNumber:
            return "021000021"

        # `issubclass` raises type error on non-classes, these must be
        # done last.
        if type_ is None or issubclass(type_, NoneType):  # type: ignore
            return None
        if issubclass(type_, Enum):
            return list(type_)[0]

        # If is child model, add type_ to processed_models and generate child.
        if issubclass(type_, BaseModel):
            return self.generate(type_, processed_models)  # type: ignore

        # Catchall.
        return type_()

    def _get_list_values(  # noqa: PLR0913
        self,
        type_: Type[Any],
        field_info: FieldInfo,
        min_length: Optional[int],
        processed_models: list[Type[ModelType]],
        *_args: Any,
        hashable: bool = False,
    ) -> list[Any]:
        target_length = min_length or default_max_len

        items: list[Any] = []
        list_types = typing.get_args(type_)
        while len(items) < target_length:
            for arg in list_types:
                if arg in processed_models:
                    return items
                value = self._get_value(
                    arg, field_info, processed_models, hashable=hashable
                )
                items.append(value)
        return items


def _get_str_value(metadata: Metadata) -> str:
    """Get a string matching length constraints."""
    default = "string"
    min_ = metadata.min_length
    max_ = metadata.max_length
    if metadata.str_constraints:
        min_ = metadata.str_constraints.min_length
        max_ = metadata.str_constraints.max_length
    if (min_ is None or min_ <= len(default)) and (
        max_ is None or max_ >= len(default)
    ):
        return default
    return "s" * (min_ or max_ or 1)


def _get_number_value(metadata: Metadata) -> AnyNumber:
    """Get a number matching certain constraints."""
    iter_size = metadata.multiple_of or 1.0

    # Determine lower bound (inclusive).
    lower = metadata.multiple_of or 0.0
    if metadata.ge is not None:
        lower = math.ceil(metadata.ge / iter_size) * iter_size
    if metadata.gt is not None and metadata.gt >= lower:
        lower = math.ceil(metadata.gt / iter_size) * iter_size
        if lower == metadata.gt:
            lower += iter_size

    # Determine upper bound (inclusive).
    upper = max(lower, metadata.multiple_of or 0.0) + iter_size
    if metadata.le is not None:
        upper = math.floor(metadata.le / iter_size) * iter_size
    if metadata.lt is not None and metadata.lt <= upper:
        upper = math.floor(metadata.lt / iter_size) * iter_size
        if upper >= metadata.lt:
            upper -= iter_size

    preferred_default_value = 1.0
    if lower <= preferred_default_value <= upper:
        return preferred_default_value
    # This will be true if lower is unset and upper is negative.
    if lower > upper:
        return upper
    # Plus iter size if possible for default of 1 rather than 0.
    return lower if lower + iter_size > upper else lower + iter_size


def _get_metadata(field_info: FieldInfo) -> Metadata:
    metadata = Metadata()
    for meta in field_info.metadata:
        if isinstance(meta, annotated_types.Gt):
            metadata.gt = meta.gt  # type: ignore
        elif isinstance(meta, annotated_types.Ge):
            metadata.ge = meta.ge  # type: ignore
        elif isinstance(meta, annotated_types.Lt):
            metadata.lt = meta.lt  # type: ignore
        elif isinstance(meta, annotated_types.Le):
            metadata.le = meta.le  # type: ignore
        elif isinstance(meta, annotated_types.MultipleOf):
            metadata.multiple_of = meta.multiple_of  # type: ignore
        elif isinstance(meta, annotated_types.MinLen):
            metadata.min_length = meta.min_length
        elif isinstance(meta, annotated_types.MaxLen):
            metadata.max_length = meta.max_length
        elif isinstance(meta, StringConstraints):
            metadata.str_constraints = meta
    return metadata


def _is_union(origin: Any) -> bool:
    try:
        # Python3.10 union types need to be checked differently.
        return origin is Union or origin.__name__ == "UnionType"
    except AttributeError:
        return False
