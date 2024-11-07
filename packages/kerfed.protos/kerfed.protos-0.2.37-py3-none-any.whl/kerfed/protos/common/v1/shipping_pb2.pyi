"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
*
shipping.proto

Get committed prices (`Rate`) for heterogenous shipments of
multiple items with different size, origin, and destination
and then buy that rate (`Label`) using the committed price.
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import kerfed.protos.common.v1.address_pb2
import kerfed.protos.common.v1.fileblob_pb2
import kerfed.protos.common.v1.money_pb2
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class ShippingRate(google.protobuf.message.Message):
    """a rate is a fully-quoted purchasable shipping option."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PRICE_FIELD_NUMBER: builtins.int
    PARCELS_FIELD_NUMBER: builtins.int
    @property
    def price(self) -> kerfed.protos.common.v1.money_pb2.Money:
        """how much does this method cost in total"""
    @property
    def parcels(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ShippingParcel]:
        """may contain different shippers"""
    def __init__(
        self,
        *,
        price: kerfed.protos.common.v1.money_pb2.Money | None = ...,
        parcels: collections.abc.Iterable[global___ShippingParcel] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["price", b"price"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["parcels", b"parcels", "price", b"price"]) -> None: ...

global___ShippingRate = ShippingRate

@typing_extensions.final
class ShippingParcel(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SHIP_FROM_FIELD_NUMBER: builtins.int
    SHIP_TO_FIELD_NUMBER: builtins.int
    LINE_ID_FIELD_NUMBER: builtins.int
    EXTENTS_FIELD_NUMBER: builtins.int
    WEIGHT_FIELD_NUMBER: builtins.int
    PROVIDER_FIELD_NUMBER: builtins.int
    PROVIDER_ID_FIELD_NUMBER: builtins.int
    LABEL_FIELD_NUMBER: builtins.int
    TRACKING_URL_FIELD_NUMBER: builtins.int
    @property
    def ship_from(self) -> kerfed.protos.common.v1.address_pb2.PostalAddress: ...
    @property
    def ship_to(self) -> kerfed.protos.common.v1.address_pb2.PostalAddress: ...
    @property
    def line_id(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """which of the LinePrice parts are contained in this parcel."""
    @property
    def extents(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """the 3D bounding box for one parcel in meters"""
    weight: builtins.float
    """the weight of the parcel in kilograms"""
    provider: builtins.str
    """i.e. "shippo", "shipengine", "easypost" """
    provider_id: builtins.str
    """the unique identifier used to purchase the label"""
    @property
    def label(self) -> kerfed.protos.common.v1.fileblob_pb2.FileBlob:
        """i.e. a PNG shipping label
        (Only populated after purchase.)
        """
    tracking_url: builtins.str
    """a tracking url
    (Only populated after purchase.)
    """
    def __init__(
        self,
        *,
        ship_from: kerfed.protos.common.v1.address_pb2.PostalAddress | None = ...,
        ship_to: kerfed.protos.common.v1.address_pb2.PostalAddress | None = ...,
        line_id: collections.abc.Iterable[builtins.str] | None = ...,
        extents: collections.abc.Iterable[builtins.float] | None = ...,
        weight: builtins.float = ...,
        provider: builtins.str = ...,
        provider_id: builtins.str = ...,
        label: kerfed.protos.common.v1.fileblob_pb2.FileBlob | None = ...,
        tracking_url: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["label", b"label", "ship_from", b"ship_from", "ship_to", b"ship_to"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["extents", b"extents", "label", b"label", "line_id", b"line_id", "provider", b"provider", "provider_id", b"provider_id", "ship_from", b"ship_from", "ship_to", b"ship_to", "tracking_url", b"tracking_url", "weight", b"weight"]) -> None: ...

global___ShippingParcel = ShippingParcel
