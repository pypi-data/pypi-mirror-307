from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="CalculatedPositionState")


@_attrs_define
class CalculatedPositionState:
    """The dynamic (calculated) state of a Position

    Attributes:
        instrument (Union[Unset, str]): The Position's Instrument.
        net_unrealized_pl (Union[Unset, str]): The Position's net unrealized profit/loss
        long_unrealized_pl (Union[Unset, str]): The unrealized profit/loss of the Position's long open Trades
        short_unrealized_pl (Union[Unset, str]): The unrealized profit/loss of the Position's short open Trades
        margin_used (Union[Unset, str]): Margin currently used by the Position.
    """

    instrument: Union[Unset, str] = UNSET
    net_unrealized_pl: Union[Unset, str] = UNSET
    long_unrealized_pl: Union[Unset, str] = UNSET
    short_unrealized_pl: Union[Unset, str] = UNSET
    margin_used: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        instrument = self.instrument

        net_unrealized_pl = self.net_unrealized_pl

        long_unrealized_pl = self.long_unrealized_pl

        short_unrealized_pl = self.short_unrealized_pl

        margin_used = self.margin_used

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if instrument is not UNSET:
            field_dict["instrument"] = instrument
        if net_unrealized_pl is not UNSET:
            field_dict["netUnrealizedPL"] = net_unrealized_pl
        if long_unrealized_pl is not UNSET:
            field_dict["longUnrealizedPL"] = long_unrealized_pl
        if short_unrealized_pl is not UNSET:
            field_dict["shortUnrealizedPL"] = short_unrealized_pl
        if margin_used is not UNSET:
            field_dict["marginUsed"] = margin_used

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        instrument = d.pop("instrument", UNSET)

        net_unrealized_pl = d.pop("netUnrealizedPL", UNSET)

        long_unrealized_pl = d.pop("longUnrealizedPL", UNSET)

        short_unrealized_pl = d.pop("shortUnrealizedPL", UNSET)

        margin_used = d.pop("marginUsed", UNSET)

        calculated_position_state = cls(
            instrument=instrument,
            net_unrealized_pl=net_unrealized_pl,
            long_unrealized_pl=long_unrealized_pl,
            short_unrealized_pl=short_unrealized_pl,
            margin_used=margin_used,
        )

        calculated_position_state.additional_properties = d
        return calculated_position_state

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
