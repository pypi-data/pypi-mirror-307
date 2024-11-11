from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .order_cancel_transaction import OrderCancelTransaction
from .order_fill_transaction import OrderFillTransaction
from .stop_loss_order_transaction import StopLossOrderTransaction
from .take_profit_order_transaction import TakeProfitOrderTransaction
from .trailing_stop_loss_order_transaction import TrailingStopLossOrderTransaction
from types import UNSET, Unset
from typing import TypeVar
from typing import List
from typing import Union

T = TypeVar("T", bound="SetTradeDependentOrdersResponse200")


@dataclasses.dataclass
class SetTradeDependentOrdersResponse200:
    """Attributes:
    take_profit_order_cancel_transaction (Union[Unset, OrderCancelTransaction]): An OrderCancelTransaction
        represents the cancellation of an Order in the client's Account.
    take_profit_order_transaction (Union[Unset, TakeProfitOrderTransaction]): A TakeProfitOrderTransaction
        represents the creation of a TakeProfit Order in the user's Account.
    take_profit_order_fill_transaction (Union[Unset, OrderFillTransaction]): An OrderFillTransaction represents the
        filling of an Order in the client's Account.
    take_profit_order_created_cancel_transaction (Union[Unset, OrderCancelTransaction]): An OrderCancelTransaction
        represents the cancellation of an Order in the client's Account.
    stop_loss_order_cancel_transaction (Union[Unset, OrderCancelTransaction]): An OrderCancelTransaction represents
        the cancellation of an Order in the client's Account.
    stop_loss_order_transaction (Union[Unset, StopLossOrderTransaction]): A StopLossOrderTransaction represents the
        creation of a StopLoss Order in the user's Account.
    stop_loss_order_fill_transaction (Union[Unset, OrderFillTransaction]): An OrderFillTransaction represents the
        filling of an Order in the client's Account.
    stop_loss_order_created_cancel_transaction (Union[Unset, OrderCancelTransaction]): An OrderCancelTransaction
        represents the cancellation of an Order in the client's Account.
    trailing_stop_loss_order_cancel_transaction (Union[Unset, OrderCancelTransaction]): An OrderCancelTransaction
        represents the cancellation of an Order in the client's Account.
    trailing_stop_loss_order_transaction (Union[Unset, TrailingStopLossOrderTransaction]): A
        TrailingStopLossOrderTransaction represents the creation of a TrailingStopLoss Order in the user's Account.
    related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
        satisfying the request.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    take_profit_order_cancel_transaction: Union[Unset, "OrderCancelTransaction"] = UNSET
    take_profit_order_transaction: Union[Unset, "TakeProfitOrderTransaction"] = UNSET
    take_profit_order_fill_transaction: Union[Unset, "OrderFillTransaction"] = UNSET
    take_profit_order_created_cancel_transaction: Union[
        Unset, "OrderCancelTransaction"
    ] = UNSET
    stop_loss_order_cancel_transaction: Union[Unset, "OrderCancelTransaction"] = UNSET
    stop_loss_order_transaction: Union[Unset, "StopLossOrderTransaction"] = UNSET
    stop_loss_order_fill_transaction: Union[Unset, "OrderFillTransaction"] = UNSET
    stop_loss_order_created_cancel_transaction: Union[
        Unset, "OrderCancelTransaction"
    ] = UNSET
    trailing_stop_loss_order_cancel_transaction: Union[
        Unset, "OrderCancelTransaction"
    ] = UNSET
    trailing_stop_loss_order_transaction: Union[
        Unset, "TrailingStopLossOrderTransaction"
    ] = UNSET
    related_transaction_i_ds: Union[Unset, List[str]] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SetTradeDependentOrdersResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
