"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
model.proto

A simple serialized mathematical model.
i.e. polynomial, piecewise, etc.
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _ModelKind:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _ModelKindEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_ModelKind.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    MODEL_KIND_UNSPECIFIED: _ModelKind.ValueType  # 0
    MODEL_KIND_CONSTANT: _ModelKind.ValueType  # 1
    """A single value."""
    MODEL_KIND_TABLE: _ModelKind.ValueType  # 2
    """A lookup table."""
    MODEL_KIND_EXPRESSION: _ModelKind.ValueType  # 3
    """A full algebraic expression"""
    MODEL_KIND_POLYNOMIAL: _ModelKind.ValueType  # 4
    """A polynomial function."""
    MODEL_KIND_POWER: _ModelKind.ValueType  # 5
    """A finite power series."""

class ModelKind(_ModelKind, metaclass=_ModelKindEnumTypeWrapper):
    """What type of math function is this?"""

MODEL_KIND_UNSPECIFIED: ModelKind.ValueType  # 0
MODEL_KIND_CONSTANT: ModelKind.ValueType  # 1
"""A single value."""
MODEL_KIND_TABLE: ModelKind.ValueType  # 2
"""A lookup table."""
MODEL_KIND_EXPRESSION: ModelKind.ValueType  # 3
"""A full algebraic expression"""
MODEL_KIND_POLYNOMIAL: ModelKind.ValueType  # 4
"""A polynomial function."""
MODEL_KIND_POWER: ModelKind.ValueType  # 5
"""A finite power series."""
global___ModelKind = ModelKind

@typing_extensions.final
class Interval(google.protobuf.message.Message):
    """Define an interval with a minimum and maximum value"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MIN_FIELD_NUMBER: builtins.int
    MAX_FIELD_NUMBER: builtins.int
    min: builtins.float
    max: builtins.float
    def __init__(
        self,
        *,
        min: builtins.float = ...,
        max: builtins.float = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["max", b"max", "min", b"min"]) -> None: ...

global___Interval = Interval

@typing_extensions.final
class Model(google.protobuf.message.Message):
    """A simple `f(x) = y` defined as a serialized message.
    This is useful for things like feed-rate curves where
    cutting speed is a function of thickness.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KIND_FIELD_NUMBER: builtins.int
    MODEL_ID_FIELD_NUMBER: builtins.int
    UNITS_FIELD_NUMBER: builtins.int
    KEYS_FIELD_NUMBER: builtins.int
    VALUES_FIELD_NUMBER: builtins.int
    EXPRESSION_FIELD_NUMBER: builtins.int
    IS_INTERPOLATED_FIELD_NUMBER: builtins.int
    LIMITS_FIELD_NUMBER: builtins.int
    kind: global___ModelKind.ValueType
    """i.e. `constant`, `polynomial`, `table`, `expression`"""
    model_id: builtins.str
    """a globally unique identitier
    i.e. a UUID: '83c96039-e77f-4603-a1f0-1a6381de159c'
    """
    @property
    def units(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """the units of the X and Y axis
        i.e. for feed rate: ["inch", "inch/minute"]
        so if you evaluate this model with X in "inch"
        it produces an "inch/minute" result
        """
    @property
    def keys(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """i.e for `kind=table`, `keys`` is the X value
        and `values` is the corresponding Y value.
        """
    @property
    def values(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]: ...
    expression: builtins.str
    """if we have an `expression` kind -_-
    i.e. "2.9 * volume_support + 1.2 * volume"
    """
    is_interpolated: builtins.bool
    """is this model allowed to be interpolated
    this is only used for `kind="table"`
    where if the exact value isn't in the table
    it will return a NaN rather than the interpolated result
    """
    @property
    def limits(self) -> global___Interval:
        """If this is defined enforce a range limit on the
        values this `Model` is allowed to be evaluated over.
        """
    def __init__(
        self,
        *,
        kind: global___ModelKind.ValueType = ...,
        model_id: builtins.str = ...,
        units: collections.abc.Iterable[builtins.str] | None = ...,
        keys: collections.abc.Iterable[builtins.float] | None = ...,
        values: collections.abc.Iterable[builtins.float] | None = ...,
        expression: builtins.str = ...,
        is_interpolated: builtins.bool = ...,
        limits: global___Interval | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["limits", b"limits"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["expression", b"expression", "is_interpolated", b"is_interpolated", "keys", b"keys", "kind", b"kind", "limits", b"limits", "model_id", b"model_id", "units", b"units", "values", b"values"]) -> None: ...

global___Model = Model
