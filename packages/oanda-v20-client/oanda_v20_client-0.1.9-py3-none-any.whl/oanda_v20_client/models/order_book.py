from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.order_book_bucket import OrderBookBucket


T = TypeVar("T", bound="OrderBook")


@_attrs_define
class OrderBook:
    """The representation of an instrument's order book at a point in time

    Attributes:
        instrument (Union[Unset, str]): The order book's instrument
        time (Union[Unset, str]): The time when the order book snapshot was created.
        price (Union[Unset, str]): The price (midpoint) for the order book's instrument at the time of the order book
            snapshot
        bucket_width (Union[Unset, str]): The price width for each bucket. Each bucket covers the price range from the
            bucket's price to the bucket's price + bucketWidth.
        buckets (Union[Unset, List['OrderBookBucket']]): The partitioned order book, divided into buckets using a
            default bucket width. These buckets are only provided for price ranges which actually contain order or position
            data.
    """

    instrument: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    price: Union[Unset, str] = UNSET
    bucket_width: Union[Unset, str] = UNSET
    buckets: Union[Unset, List["OrderBookBucket"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        instrument = self.instrument

        time = self.time

        price = self.price

        bucket_width = self.bucket_width

        buckets: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.buckets, Unset):
            buckets = []
            for buckets_item_data in self.buckets:
                buckets_item = buckets_item_data.to_dict()
                buckets.append(buckets_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if instrument is not UNSET:
            field_dict["instrument"] = instrument
        if time is not UNSET:
            field_dict["time"] = time
        if price is not UNSET:
            field_dict["price"] = price
        if bucket_width is not UNSET:
            field_dict["bucketWidth"] = bucket_width
        if buckets is not UNSET:
            field_dict["buckets"] = buckets

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.order_book_bucket import OrderBookBucket

        d = src_dict.copy()
        instrument = d.pop("instrument", UNSET)

        time = d.pop("time", UNSET)

        price = d.pop("price", UNSET)

        bucket_width = d.pop("bucketWidth", UNSET)

        buckets = []
        _buckets = d.pop("buckets", UNSET)
        for buckets_item_data in _buckets or []:
            buckets_item = OrderBookBucket.from_dict(buckets_item_data)

            buckets.append(buckets_item)

        order_book = cls(
            instrument=instrument,
            time=time,
            price=price,
            bucket_width=bucket_width,
            buckets=buckets,
        )

        order_book.additional_properties = d
        return order_book

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
