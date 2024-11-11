from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .order_cancel_reject_transaction import OrderCancelRejectTransaction
from .stop_loss_order_reject_transaction import StopLossOrderRejectTransaction
from .take_profit_order_reject_transaction import TakeProfitOrderRejectTransaction
from .trailing_stop_loss_order_reject_transaction import (
    TrailingStopLossOrderRejectTransaction,
)
from types import UNSET, Unset
from typing import TypeVar
from typing import List
from typing import Union

T = TypeVar("T", bound="SetTradeDependentOrdersResponse400")


@dataclasses.dataclass
class SetTradeDependentOrdersResponse400:
    """Attributes:
    take_profit_order_cancel_reject_transaction (Union[Unset, OrderCancelRejectTransaction]): An
        OrderCancelRejectTransaction represents the rejection of the cancellation of an Order in the client's Account.
    take_profit_order_reject_transaction (Union[Unset, TakeProfitOrderRejectTransaction]): A
        TakeProfitOrderRejectTransaction represents the rejection of the creation of a TakeProfit Order.
    stop_loss_order_cancel_reject_transaction (Union[Unset, OrderCancelRejectTransaction]): An
        OrderCancelRejectTransaction represents the rejection of the cancellation of an Order in the client's Account.
    stop_loss_order_reject_transaction (Union[Unset, StopLossOrderRejectTransaction]): A
        StopLossOrderRejectTransaction represents the rejection of the creation of a StopLoss Order.
    trailing_stop_loss_order_cancel_reject_transaction (Union[Unset, OrderCancelRejectTransaction]): An
        OrderCancelRejectTransaction represents the rejection of the cancellation of an Order in the client's Account.
    trailing_stop_loss_order_reject_transaction (Union[Unset, TrailingStopLossOrderRejectTransaction]): A
        TrailingStopLossOrderRejectTransaction represents the rejection of the creation of a TrailingStopLoss Order.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account.
    related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
        satisfying the request.
    error_code (Union[Unset, str]): The code of the error that has occurred. This field may not be returned for some
        errors.
    error_message (Union[Unset, str]): The human-readable description of the error that has occurred."""

    take_profit_order_cancel_reject_transaction: Union[
        Unset, "OrderCancelRejectTransaction"
    ] = UNSET
    take_profit_order_reject_transaction: Union[
        Unset, "TakeProfitOrderRejectTransaction"
    ] = UNSET
    stop_loss_order_cancel_reject_transaction: Union[
        Unset, "OrderCancelRejectTransaction"
    ] = UNSET
    stop_loss_order_reject_transaction: Union[
        Unset, "StopLossOrderRejectTransaction"
    ] = UNSET
    trailing_stop_loss_order_cancel_reject_transaction: Union[
        Unset, "OrderCancelRejectTransaction"
    ] = UNSET
    trailing_stop_loss_order_reject_transaction: Union[
        Unset, "TrailingStopLossOrderRejectTransaction"
    ] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    related_transaction_i_ds: Union[Unset, List[str]] = UNSET
    error_code: Union[Unset, str] = UNSET
    error_message: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SetTradeDependentOrdersResponse400":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
