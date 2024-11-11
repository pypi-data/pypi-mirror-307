from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .order_cancel_transaction import OrderCancelTransaction
from .order_fill_transaction import OrderFillTransaction
from .stop_loss_order_transaction import StopLossOrderTransaction
from .take_profit_order_transaction import TakeProfitOrderTransaction
from .trailing_stop_loss_order_transaction import TrailingStopLossOrderTransaction
from types import Unset
from typing import List, Optional, Type, TypeVar, cast

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

    take_profit_order_cancel_transaction: Optional["OrderCancelTransaction"]
    take_profit_order_transaction: Optional["TakeProfitOrderTransaction"]
    take_profit_order_fill_transaction: Optional["OrderFillTransaction"]
    take_profit_order_created_cancel_transaction: Optional["OrderCancelTransaction"]
    stop_loss_order_cancel_transaction: Optional["OrderCancelTransaction"]
    stop_loss_order_transaction: Optional["StopLossOrderTransaction"]
    stop_loss_order_fill_transaction: Optional["OrderFillTransaction"]
    stop_loss_order_created_cancel_transaction: Optional["OrderCancelTransaction"]
    trailing_stop_loss_order_cancel_transaction: Optional["OrderCancelTransaction"]
    trailing_stop_loss_order_transaction: Optional["TrailingStopLossOrderTransaction"]
    related_transaction_i_ds: Optional[List[str]]
    last_transaction_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .order_cancel_transaction import OrderCancelTransaction
        from .order_fill_transaction import OrderFillTransaction
        from .stop_loss_order_transaction import StopLossOrderTransaction
        from .take_profit_order_transaction import TakeProfitOrderTransaction
        from .trailing_stop_loss_order_transaction import (
            TrailingStopLossOrderTransaction,
        )

        d = src_dict.copy()
        _take_profit_order_cancel_transaction = d.pop(
            "takeProfitOrderCancelTransaction", None
        )
        take_profit_order_cancel_transaction: Optional[OrderCancelTransaction]
        if isinstance(_take_profit_order_cancel_transaction, Unset):
            take_profit_order_cancel_transaction = None
        else:
            take_profit_order_cancel_transaction = OrderCancelTransaction.from_dict(
                _take_profit_order_cancel_transaction
            )
        _take_profit_order_transaction = d.pop("takeProfitOrderTransaction", None)
        take_profit_order_transaction: Optional[TakeProfitOrderTransaction]
        if isinstance(_take_profit_order_transaction, Unset):
            take_profit_order_transaction = None
        else:
            take_profit_order_transaction = TakeProfitOrderTransaction.from_dict(
                _take_profit_order_transaction
            )
        _take_profit_order_fill_transaction = d.pop(
            "takeProfitOrderFillTransaction", None
        )
        take_profit_order_fill_transaction: Optional[OrderFillTransaction]
        if isinstance(_take_profit_order_fill_transaction, Unset):
            take_profit_order_fill_transaction = None
        else:
            take_profit_order_fill_transaction = OrderFillTransaction.from_dict(
                _take_profit_order_fill_transaction
            )
        _take_profit_order_created_cancel_transaction = d.pop(
            "takeProfitOrderCreatedCancelTransaction", None
        )
        take_profit_order_created_cancel_transaction: Optional[OrderCancelTransaction]
        if isinstance(_take_profit_order_created_cancel_transaction, Unset):
            take_profit_order_created_cancel_transaction = None
        else:
            take_profit_order_created_cancel_transaction = (
                OrderCancelTransaction.from_dict(
                    _take_profit_order_created_cancel_transaction
                )
            )
        _stop_loss_order_cancel_transaction = d.pop(
            "stopLossOrderCancelTransaction", None
        )
        stop_loss_order_cancel_transaction: Optional[OrderCancelTransaction]
        if isinstance(_stop_loss_order_cancel_transaction, Unset):
            stop_loss_order_cancel_transaction = None
        else:
            stop_loss_order_cancel_transaction = OrderCancelTransaction.from_dict(
                _stop_loss_order_cancel_transaction
            )
        _stop_loss_order_transaction = d.pop("stopLossOrderTransaction", None)
        stop_loss_order_transaction: Optional[StopLossOrderTransaction]
        if isinstance(_stop_loss_order_transaction, Unset):
            stop_loss_order_transaction = None
        else:
            stop_loss_order_transaction = StopLossOrderTransaction.from_dict(
                _stop_loss_order_transaction
            )
        _stop_loss_order_fill_transaction = d.pop("stopLossOrderFillTransaction", None)
        stop_loss_order_fill_transaction: Optional[OrderFillTransaction]
        if isinstance(_stop_loss_order_fill_transaction, Unset):
            stop_loss_order_fill_transaction = None
        else:
            stop_loss_order_fill_transaction = OrderFillTransaction.from_dict(
                _stop_loss_order_fill_transaction
            )
        _stop_loss_order_created_cancel_transaction = d.pop(
            "stopLossOrderCreatedCancelTransaction", None
        )
        stop_loss_order_created_cancel_transaction: Optional[OrderCancelTransaction]
        if isinstance(_stop_loss_order_created_cancel_transaction, Unset):
            stop_loss_order_created_cancel_transaction = None
        else:
            stop_loss_order_created_cancel_transaction = (
                OrderCancelTransaction.from_dict(
                    _stop_loss_order_created_cancel_transaction
                )
            )
        _trailing_stop_loss_order_cancel_transaction = d.pop(
            "trailingStopLossOrderCancelTransaction", None
        )
        trailing_stop_loss_order_cancel_transaction: Optional[OrderCancelTransaction]
        if isinstance(_trailing_stop_loss_order_cancel_transaction, Unset):
            trailing_stop_loss_order_cancel_transaction = None
        else:
            trailing_stop_loss_order_cancel_transaction = (
                OrderCancelTransaction.from_dict(
                    _trailing_stop_loss_order_cancel_transaction
                )
            )
        _trailing_stop_loss_order_transaction = d.pop(
            "trailingStopLossOrderTransaction", None
        )
        trailing_stop_loss_order_transaction: Optional[TrailingStopLossOrderTransaction]
        if isinstance(_trailing_stop_loss_order_transaction, Unset):
            trailing_stop_loss_order_transaction = None
        else:
            trailing_stop_loss_order_transaction = (
                TrailingStopLossOrderTransaction.from_dict(
                    _trailing_stop_loss_order_transaction
                )
            )
        related_transaction_i_ds = cast(List[str], d.pop("relatedTransactionIDs", None))
        last_transaction_id = d.pop("lastTransactionID", None)
        set_trade_dependent_orders_response_200 = cls(
            take_profit_order_cancel_transaction=take_profit_order_cancel_transaction,
            take_profit_order_transaction=take_profit_order_transaction,
            take_profit_order_fill_transaction=take_profit_order_fill_transaction,
            take_profit_order_created_cancel_transaction=take_profit_order_created_cancel_transaction,
            stop_loss_order_cancel_transaction=stop_loss_order_cancel_transaction,
            stop_loss_order_transaction=stop_loss_order_transaction,
            stop_loss_order_fill_transaction=stop_loss_order_fill_transaction,
            stop_loss_order_created_cancel_transaction=stop_loss_order_created_cancel_transaction,
            trailing_stop_loss_order_cancel_transaction=trailing_stop_loss_order_cancel_transaction,
            trailing_stop_loss_order_transaction=trailing_stop_loss_order_transaction,
            related_transaction_i_ds=related_transaction_i_ds,
            last_transaction_id=last_transaction_id,
        )
        set_trade_dependent_orders_response_200.additional_properties = d
        return set_trade_dependent_orders_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
