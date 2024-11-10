from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.guaranteed_stop_loss_order_level_restriction import (
        GuaranteedStopLossOrderLevelRestriction,
    )


T = TypeVar("T", bound="GuaranteedStopLossOrderEntryData")


@_attrs_define
class GuaranteedStopLossOrderEntryData:
    """Details required by clients creating a Guaranteed Stop Loss Order

    Attributes:
        minimum_distance (Union[Unset, str]): The minimum distance allowed between the Trade's fill price and the
            configured price for guaranteed Stop Loss Orders created for this instrument. Specified in price units.
        premium (Union[Unset, str]): The amount that is charged to the account if a guaranteed Stop Loss Order is
            triggered and filled. The value is in price units and is charged for each unit of the Trade.
        level_restriction (Union[Unset, GuaranteedStopLossOrderLevelRestriction]): A
            GuaranteedStopLossOrderLevelRestriction represents the total position size that can exist within a given price
            window for Trades with guaranteed Stop Loss Orders attached for a specific Instrument.
    """

    minimum_distance: Union[Unset, str] = UNSET
    premium: Union[Unset, str] = UNSET
    level_restriction: Union[Unset, "GuaranteedStopLossOrderLevelRestriction"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        minimum_distance = self.minimum_distance

        premium = self.premium

        level_restriction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.level_restriction, Unset):
            level_restriction = self.level_restriction.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if minimum_distance is not UNSET:
            field_dict["minimumDistance"] = minimum_distance
        if premium is not UNSET:
            field_dict["premium"] = premium
        if level_restriction is not UNSET:
            field_dict["levelRestriction"] = level_restriction

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.guaranteed_stop_loss_order_level_restriction import (
            GuaranteedStopLossOrderLevelRestriction,
        )

        d = src_dict.copy()
        minimum_distance = d.pop("minimumDistance", UNSET)

        premium = d.pop("premium", UNSET)

        _level_restriction = d.pop("levelRestriction", UNSET)
        level_restriction: Union[Unset, GuaranteedStopLossOrderLevelRestriction]
        if isinstance(_level_restriction, Unset):
            level_restriction = UNSET
        else:
            level_restriction = GuaranteedStopLossOrderLevelRestriction.from_dict(
                _level_restriction
            )

        guaranteed_stop_loss_order_entry_data = cls(
            minimum_distance=minimum_distance,
            premium=premium,
            level_restriction=level_restriction,
        )

        guaranteed_stop_loss_order_entry_data.additional_properties = d
        return guaranteed_stop_loss_order_entry_data

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
