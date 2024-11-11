from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="DynamicOrderState")


@dataclasses.dataclass
class DynamicOrderState:
    """The dynamic state of an Order. This is only relevant to TrailingStopLoss Orders, as no other Order type has dynamic
    state.

        Attributes:
            id (Union[Unset, str]): The Order's ID.
            trailing_stop_value (Union[Unset, str]): The Order's calculated trailing stop value.
            trigger_distance (Union[Unset, str]): The distance between the Trailing Stop Loss Order's trailingStopValue and
                the current Market Price. This represents the distance (in price units) of the Order from a triggering price. If
                the distance could not be determined, this value will not be set.
            is_trigger_distance_exact (Union[Unset, bool]): True if an exact trigger distance could be calculated. If false,
                it means the provided trigger distance is a best estimate. If the distance could not be determined, this value
                will not be set."""

    id: Optional[str]
    trailing_stop_value: Optional[str]
    trigger_distance: Optional[str]
    is_trigger_distance_exact: Optional[bool]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", None)
        trailing_stop_value = d.pop("trailingStopValue", None)
        trigger_distance = d.pop("triggerDistance", None)
        is_trigger_distance_exact = d.pop("isTriggerDistanceExact", None)
        dynamic_order_state = cls(
            id=id,
            trailing_stop_value=trailing_stop_value,
            trigger_distance=trigger_distance,
            is_trigger_distance_exact=is_trigger_distance_exact,
        )
        dynamic_order_state.additional_properties = d
        return dynamic_order_state

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
