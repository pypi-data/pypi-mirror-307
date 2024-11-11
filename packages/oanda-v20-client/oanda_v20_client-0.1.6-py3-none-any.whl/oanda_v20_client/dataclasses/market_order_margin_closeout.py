from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .market_order_margin_closeout_reason import MarketOrderMarginCloseoutReason
from typing import Optional, TypeVar

T = TypeVar("T", bound="MarketOrderMarginCloseout")


@dataclasses.dataclass
class MarketOrderMarginCloseout:
    """Details for the Market Order extensions specific to a Market Order placed that is part of a Market Order Margin
    Closeout in a client's account

        Attributes:
            reason (Union[Unset, MarketOrderMarginCloseoutReason]): The reason the Market Order was created to perform a
                margin closeout"""

    reason: Optional[MarketOrderMarginCloseoutReason]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MarketOrderMarginCloseout":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
