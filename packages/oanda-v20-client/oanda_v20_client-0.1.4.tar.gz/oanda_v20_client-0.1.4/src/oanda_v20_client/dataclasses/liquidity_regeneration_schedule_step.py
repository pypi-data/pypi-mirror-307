from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from typing import TypeVar, Union

T = TypeVar("T", bound="LiquidityRegenerationScheduleStep")


@dataclasses.dataclass
class LiquidityRegenerationScheduleStep:
    """A liquidity regeneration schedule Step indicates the amount of bid and ask liquidity that is used by the Account at
    a certain time. These amounts will only change at the timestamp of the following step.

        Attributes:
            timestamp (Union[Unset, str]): The timestamp of the schedule step.
            bid_liquidity_used (Union[Unset, str]): The amount of bid liquidity used at this step in the schedule.
            ask_liquidity_used (Union[Unset, str]): The amount of ask liquidity used at this step in the schedule."""

    timestamp: Union[Unset, str] = UNSET
    bid_liquidity_used: Union[Unset, str] = UNSET
    ask_liquidity_used: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LiquidityRegenerationScheduleStep":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
