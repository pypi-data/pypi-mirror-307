from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="PriceBucket")


@_attrs_define
class PriceBucket:
    """A Price Bucket represents a price available for an amount of liquidity

    Attributes:
        price (Union[Unset, str]): The Price offered by the PriceBucket
        liquidity (Union[Unset, int]): The amount of liquidity offered by the PriceBucket
    """

    price: Union[Unset, str] = UNSET
    liquidity: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        price = self.price

        liquidity = self.liquidity

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if price is not UNSET:
            field_dict["price"] = price
        if liquidity is not UNSET:
            field_dict["liquidity"] = liquidity

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        price = d.pop("price", UNSET)

        liquidity = d.pop("liquidity", UNSET)

        price_bucket = cls(
            price=price,
            liquidity=liquidity,
        )

        price_bucket.additional_properties = d
        return price_bucket

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
