from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.price import Price


T = TypeVar("T", bound="GetInstrumentPriceRangeResponse200")


@_attrs_define
class GetInstrumentPriceRangeResponse200:
    """
    Attributes:
        prices (Union[Unset, List['Price']]): The list of prices that satisfy the request.
    """

    prices: Union[Unset, List["Price"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prices: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.prices, Unset):
            prices = []
            for prices_item_data in self.prices:
                prices_item = prices_item_data.to_dict()
                prices.append(prices_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if prices is not UNSET:
            field_dict["prices"] = prices

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.price import Price

        d = src_dict.copy()
        prices = []
        _prices = d.pop("prices", UNSET)
        for prices_item_data in _prices or []:
            prices_item = Price.from_dict(prices_item_data)

            prices.append(prices_item)

        get_instrument_price_range_response_200 = cls(
            prices=prices,
        )

        get_instrument_price_range_response_200.additional_properties = d
        return get_instrument_price_range_response_200

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
