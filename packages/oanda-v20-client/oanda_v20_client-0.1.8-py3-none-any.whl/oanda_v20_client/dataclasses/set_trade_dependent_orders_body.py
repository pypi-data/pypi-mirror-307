from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .stop_loss_details import StopLossDetails
from .take_profit_details import TakeProfitDetails
from .trailing_stop_loss_details import TrailingStopLossDetails
from types import Unset
from typing import Optional, Type, TypeVar

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

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .stop_loss_details import StopLossDetails
        from .trailing_stop_loss_details import TrailingStopLossDetails
        from .take_profit_details import TakeProfitDetails

        d = src_dict.copy()
        _take_profit = d.pop("takeProfit", None)
        take_profit: Optional[TakeProfitDetails]
        if isinstance(_take_profit, Unset):
            take_profit = None
        else:
            take_profit = TakeProfitDetails.from_dict(_take_profit)
        _stop_loss = d.pop("stopLoss", None)
        stop_loss: Optional[StopLossDetails]
        if isinstance(_stop_loss, Unset):
            stop_loss = None
        else:
            stop_loss = StopLossDetails.from_dict(_stop_loss)
        _trailing_stop_loss = d.pop("trailingStopLoss", None)
        trailing_stop_loss: Optional[TrailingStopLossDetails]
        if isinstance(_trailing_stop_loss, Unset):
            trailing_stop_loss = None
        else:
            trailing_stop_loss = TrailingStopLossDetails.from_dict(_trailing_stop_loss)
        set_trade_dependent_orders_body = cls(
            take_profit=take_profit,
            stop_loss=stop_loss,
            trailing_stop_loss=trailing_stop_loss,
        )
        set_trade_dependent_orders_body.additional_properties = d
        return set_trade_dependent_orders_body

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
