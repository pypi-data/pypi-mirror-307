"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _UnitSystem:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _UnitSystemEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_UnitSystem.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    UNIT_SYSTEM_UNSPECIFIED: _UnitSystem.ValueType  # 0
    """If unspecified units in the parent message are
    assumed to be "meters-kilograms-seconds"
    """
    UNIT_SYSTEM_MKS: _UnitSystem.ValueType  # 1
    """All units in the parent message are `meters-kilograms-seconds`"""
    UNIT_SYSTEM_IPS: _UnitSystem.ValueType  # 2
    """All units in the parent message are `inches-pounds-seconds`"""

class UnitSystem(_UnitSystem, metaclass=_UnitSystemEnumTypeWrapper): ...

UNIT_SYSTEM_UNSPECIFIED: UnitSystem.ValueType  # 0
"""If unspecified units in the parent message are
assumed to be "meters-kilograms-seconds"
"""
UNIT_SYSTEM_MKS: UnitSystem.ValueType  # 1
"""All units in the parent message are `meters-kilograms-seconds`"""
UNIT_SYSTEM_IPS: UnitSystem.ValueType  # 2
"""All units in the parent message are `inches-pounds-seconds`"""
global___UnitSystem = UnitSystem
