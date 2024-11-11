from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="LiquidityRegenerationScheduleStep")


@dataclasses.dataclass
class LiquidityRegenerationScheduleStep:
    """A liquidity regeneration schedule Step indicates the amount of bid and ask liquidity that is used by the Account at
    a certain time. These amounts will only change at the timestamp of the following step.

        Attributes:
            timestamp (Union[Unset, str]): The timestamp of the schedule step.
            bid_liquidity_used (Union[Unset, str]): The amount of bid liquidity used at this step in the schedule.
            ask_liquidity_used (Union[Unset, str]): The amount of ask liquidity used at this step in the schedule."""

    timestamp: Optional[str]
    bid_liquidity_used: Optional[str]
    ask_liquidity_used: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        timestamp = d.pop("timestamp", None)
        bid_liquidity_used = d.pop("bidLiquidityUsed", None)
        ask_liquidity_used = d.pop("askLiquidityUsed", None)
        liquidity_regeneration_schedule_step = cls(
            timestamp=timestamp,
            bid_liquidity_used=bid_liquidity_used,
            ask_liquidity_used=ask_liquidity_used,
        )
        liquidity_regeneration_schedule_step.additional_properties = d
        return liquidity_regeneration_schedule_step

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
