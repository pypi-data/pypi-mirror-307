from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .guaranteed_stop_loss_order_level_restriction import (
    GuaranteedStopLossOrderLevelRestriction,
)
from typing import Optional, TypeVar

T = TypeVar("T", bound="GuaranteedStopLossOrderEntryData")


@dataclasses.dataclass
class GuaranteedStopLossOrderEntryData:
    """Details required by clients creating a Guaranteed Stop Loss Order

    Attributes:
        minimum_distance (Union[Unset, str]): The minimum distance allowed between the Trade's fill price and the
            configured price for guaranteed Stop Loss Orders created for this instrument. Specified in price units.
        premium (Union[Unset, str]): The amount that is charged to the account if a guaranteed Stop Loss Order is
            triggered and filled. The value is in price units and is charged for each unit of the Trade.
        level_restriction (Union[Unset, GuaranteedStopLossOrderLevelRestriction]): A
            GuaranteedStopLossOrderLevelRestriction represents the total position size that can exist within a given price
            window for Trades with guaranteed Stop Loss Orders attached for a specific Instrument."""

    minimum_distance: Optional[str]
    premium: Optional[str]
    level_restriction: Optional["GuaranteedStopLossOrderLevelRestriction"]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GuaranteedStopLossOrderEntryData":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
