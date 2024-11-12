from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="CloseTradeBody")


@_attrs_define
class CloseTradeBody:
    """
    Attributes:
        units (Union[Unset, str]): Indication of how much of the Trade to close. Either the string "ALL" (indicating
            that all of the Trade should be closed), or a DecimalNumber representing the number of units of the open Trade
            to Close using a TradeClose MarketOrder. The units specified must always be positive, and the magnitude of the
            value cannot exceed the magnitude of the Trade's open units.
    """

    units: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        units = self.units

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if units is not UNSET:
            field_dict["units"] = units

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        units = d.pop("units", UNSET)

        close_trade_body = cls(
            units=units,
        )

        close_trade_body.additional_properties = d
        return close_trade_body

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
