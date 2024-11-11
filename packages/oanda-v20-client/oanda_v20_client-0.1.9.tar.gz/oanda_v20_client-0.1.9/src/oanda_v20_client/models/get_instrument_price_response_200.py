from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.price import Price


T = TypeVar("T", bound="GetInstrumentPriceResponse200")


@_attrs_define
class GetInstrumentPriceResponse200:
    """
    Attributes:
        price (Union[Unset, Price]): The Price representation
    """

    price: Union[Unset, "Price"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        price: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.price, Unset):
            price = self.price.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if price is not UNSET:
            field_dict["price"] = price

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.price import Price

        d = src_dict.copy()
        _price = d.pop("price", UNSET)
        price: Union[Unset, Price]
        if isinstance(_price, Unset):
            price = UNSET
        else:
            price = Price.from_dict(_price)

        get_instrument_price_response_200 = cls(
            price=price,
        )

        get_instrument_price_response_200.additional_properties = d
        return get_instrument_price_response_200

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
