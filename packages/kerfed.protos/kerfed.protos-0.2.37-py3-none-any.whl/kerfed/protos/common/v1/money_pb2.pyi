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
class Money(google.protobuf.message.Message):
    """Represents an amount of money with its currency type."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CURRENCY_FIELD_NUMBER: builtins.int
    AMOUNT_FIELD_NUMBER: builtins.int
    currency: builtins.str
    """The three-letter currency code defined in ISO-4217.
    if undefined it is assumed to be `USD`
    """
    amount: builtins.int
    """The amount in the smallest unit of the specified currency
    following all the rules and special cases of the Stripe
    currency representation: https://docs.stripe.com/currencies
    For example if the message was:
       `{currency: "USD", amount=1}`
    That represents one US cent ($0.01 USD).
    """
    def __init__(
        self,
        *,
        currency: builtins.str = ...,
        amount: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["amount", b"amount", "currency", b"currency"]) -> None: ...

global___Money = Money
