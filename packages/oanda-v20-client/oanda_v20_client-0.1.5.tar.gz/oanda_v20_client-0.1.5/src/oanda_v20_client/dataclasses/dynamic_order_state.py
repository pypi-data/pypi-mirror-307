from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from typing import TypeVar, Union

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

    id: Union[Unset, str] = UNSET
    trailing_stop_value: Union[Unset, str] = UNSET
    trigger_distance: Union[Unset, str] = UNSET
    is_trigger_distance_exact: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DynamicOrderState":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
