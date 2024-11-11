from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="LiquidityRegenerationScheduleStep")


@_attrs_define
class LiquidityRegenerationScheduleStep:
    """A liquidity regeneration schedule Step indicates the amount of bid and ask liquidity that is used by the Account at
    a certain time. These amounts will only change at the timestamp of the following step.

        Attributes:
            timestamp (Union[Unset, str]): The timestamp of the schedule step.
            bid_liquidity_used (Union[Unset, str]): The amount of bid liquidity used at this step in the schedule.
            ask_liquidity_used (Union[Unset, str]): The amount of ask liquidity used at this step in the schedule.
    """

    timestamp: Union[Unset, str] = UNSET
    bid_liquidity_used: Union[Unset, str] = UNSET
    ask_liquidity_used: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        timestamp = self.timestamp

        bid_liquidity_used = self.bid_liquidity_used

        ask_liquidity_used = self.ask_liquidity_used

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if bid_liquidity_used is not UNSET:
            field_dict["bidLiquidityUsed"] = bid_liquidity_used
        if ask_liquidity_used is not UNSET:
            field_dict["askLiquidityUsed"] = ask_liquidity_used

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        timestamp = d.pop("timestamp", UNSET)

        bid_liquidity_used = d.pop("bidLiquidityUsed", UNSET)

        ask_liquidity_used = d.pop("askLiquidityUsed", UNSET)

        liquidity_regeneration_schedule_step = cls(
            timestamp=timestamp,
            bid_liquidity_used=bid_liquidity_used,
            ask_liquidity_used=ask_liquidity_used,
        )

        liquidity_regeneration_schedule_step.additional_properties = d
        return liquidity_regeneration_schedule_step

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
