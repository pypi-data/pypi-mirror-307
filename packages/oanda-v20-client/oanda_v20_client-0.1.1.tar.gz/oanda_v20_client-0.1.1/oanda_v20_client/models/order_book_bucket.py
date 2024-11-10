from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="OrderBookBucket")


@_attrs_define
class OrderBookBucket:
    """The order book data for a partition of the instrument's prices.

    Attributes:
        price (Union[Unset, str]): The lowest price (inclusive) covered by the bucket. The bucket covers the price range
            from the price to price + the order book's bucketWidth.
        long_count_percent (Union[Unset, str]): The percentage of the total number of orders represented by the long
            orders found in this bucket.
        short_count_percent (Union[Unset, str]): The percentage of the total number of orders represented by the short
            orders found in this bucket.
    """

    price: Union[Unset, str] = UNSET
    long_count_percent: Union[Unset, str] = UNSET
    short_count_percent: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        price = self.price

        long_count_percent = self.long_count_percent

        short_count_percent = self.short_count_percent

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if price is not UNSET:
            field_dict["price"] = price
        if long_count_percent is not UNSET:
            field_dict["longCountPercent"] = long_count_percent
        if short_count_percent is not UNSET:
            field_dict["shortCountPercent"] = short_count_percent

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        price = d.pop("price", UNSET)

        long_count_percent = d.pop("longCountPercent", UNSET)

        short_count_percent = d.pop("shortCountPercent", UNSET)

        order_book_bucket = cls(
            price=price,
            long_count_percent=long_count_percent,
            short_count_percent=short_count_percent,
        )

        order_book_bucket.additional_properties = d
        return order_book_bucket

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
