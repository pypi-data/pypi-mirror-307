"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class Discount(google.protobuf.message.Message):
    """Represents an amount of money with its currency type."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CODE_FIELD_NUMBER: builtins.int
    PERCENT_FIELD_NUMBER: builtins.int
    code: builtins.str
    """The discount code used."""
    percent: builtins.float
    """The percentage of discount.
    Values outside of the range (0.0, 1.0) will throw errors.
    A value of `0.1` represents a 10% discount
    or $10.00 off of a $100.00 order.
    """
    def __init__(
        self,
        *,
        code: builtins.str = ...,
        percent: builtins.float = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["code", b"code", "percent", b"percent"]) -> None: ...

global___Discount = Discount
