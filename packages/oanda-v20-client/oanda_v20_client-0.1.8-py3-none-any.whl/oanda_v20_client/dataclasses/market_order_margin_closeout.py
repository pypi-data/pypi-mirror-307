from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .market_order_margin_closeout_reason import MarketOrderMarginCloseoutReason
from .market_order_margin_closeout_reason import (
    check_market_order_margin_closeout_reason,
)
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="MarketOrderMarginCloseout")


@dataclasses.dataclass
class MarketOrderMarginCloseout:
    """Details for the Market Order extensions specific to a Market Order placed that is part of a Market Order Margin
    Closeout in a client's account

        Attributes:
            reason (Union[Unset, MarketOrderMarginCloseoutReason]): The reason the Market Order was created to perform a
                margin closeout"""

    reason: Optional[MarketOrderMarginCloseoutReason]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _reason = d.pop("reason", None)
        reason: Optional[MarketOrderMarginCloseoutReason]
        if isinstance(_reason, Unset):
            reason = None
        else:
            reason = check_market_order_margin_closeout_reason(_reason)
        market_order_margin_closeout = cls(reason=reason)
        market_order_margin_closeout.additional_properties = d
        return market_order_margin_closeout

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
