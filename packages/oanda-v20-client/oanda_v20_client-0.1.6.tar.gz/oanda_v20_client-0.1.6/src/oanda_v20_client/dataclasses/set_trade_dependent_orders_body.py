from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .stop_loss_details import StopLossDetails
from .take_profit_details import TakeProfitDetails
from .trailing_stop_loss_details import TrailingStopLossDetails
from typing import Optional, TypeVar

T = TypeVar("T", bound="SetTradeDependentOrdersBody")


@dataclasses.dataclass
class SetTradeDependentOrdersBody:
    """Attributes:
    take_profit (Union[Unset, TakeProfitDetails]): TakeProfitDetails specifies the details of a Take Profit Order to
        be created on behalf of a client. This may happen when an Order is filled that opens a Trade requiring a Take
        Profit, or when a Trade's dependent Take Profit Order is modified directly through the Trade.
    stop_loss (Union[Unset, StopLossDetails]): StopLossDetails specifies the details of a Stop Loss Order to be
        created on behalf of a client. This may happen when an Order is filled that opens a Trade requiring a Stop Loss,
        or when a Trade's dependent Stop Loss Order is modified directly through the Trade.
    trailing_stop_loss (Union[Unset, TrailingStopLossDetails]): TrailingStopLossDetails specifies the details of a
        Trailing Stop Loss Order to be created on behalf of a client. This may happen when an Order is filled that opens
        a Trade requiring a Trailing Stop Loss, or when a Trade's dependent Trailing Stop Loss Order is modified
        directly through the Trade."""

    take_profit: Optional["TakeProfitDetails"]
    stop_loss: Optional["StopLossDetails"]
    trailing_stop_loss: Optional["TrailingStopLossDetails"]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SetTradeDependentOrdersBody":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
