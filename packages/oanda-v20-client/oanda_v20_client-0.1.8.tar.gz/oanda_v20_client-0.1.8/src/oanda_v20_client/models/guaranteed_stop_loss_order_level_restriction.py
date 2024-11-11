from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="GuaranteedStopLossOrderLevelRestriction")


@_attrs_define
class GuaranteedStopLossOrderLevelRestriction:
    """A GuaranteedStopLossOrderLevelRestriction represents the total position size that can exist within a given price
    window for Trades with guaranteed Stop Loss Orders attached for a specific Instrument.

        Attributes:
            volume (Union[Unset, str]): Applies to Trades with a guaranteed Stop Loss Order attached for the specified
                Instrument. This is the total allowed Trade volume that can exist within the priceRange based on the trigger
                prices of the guaranteed Stop Loss Orders.
            price_range (Union[Unset, str]): The price range the volume applies to. This value is in price units.
    """

    volume: Union[Unset, str] = UNSET
    price_range: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        volume = self.volume

        price_range = self.price_range

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if volume is not UNSET:
            field_dict["volume"] = volume
        if price_range is not UNSET:
            field_dict["priceRange"] = price_range

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        volume = d.pop("volume", UNSET)

        price_range = d.pop("priceRange", UNSET)

        guaranteed_stop_loss_order_level_restriction = cls(
            volume=volume,
            price_range=price_range,
        )

        guaranteed_stop_loss_order_level_restriction.additional_properties = d
        return guaranteed_stop_loss_order_level_restriction

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
