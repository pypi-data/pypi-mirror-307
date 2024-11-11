from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .order_cancel_reject_transaction import OrderCancelRejectTransaction
from .stop_loss_order_reject_transaction import StopLossOrderRejectTransaction
from .take_profit_order_reject_transaction import TakeProfitOrderRejectTransaction
from .trailing_stop_loss_order_reject_transaction import (
    TrailingStopLossOrderRejectTransaction,
)
from types import Unset
from typing import List, Optional, Type, TypeVar, cast

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

    take_profit_order_cancel_reject_transaction: Optional[
        "OrderCancelRejectTransaction"
    ]
    take_profit_order_reject_transaction: Optional["TakeProfitOrderRejectTransaction"]
    stop_loss_order_cancel_reject_transaction: Optional["OrderCancelRejectTransaction"]
    stop_loss_order_reject_transaction: Optional["StopLossOrderRejectTransaction"]
    trailing_stop_loss_order_cancel_reject_transaction: Optional[
        "OrderCancelRejectTransaction"
    ]
    trailing_stop_loss_order_reject_transaction: Optional[
        "TrailingStopLossOrderRejectTransaction"
    ]
    last_transaction_id: Optional[str]
    related_transaction_i_ds: Optional[List[str]]
    error_code: Optional[str]
    error_message: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .trailing_stop_loss_order_reject_transaction import (
            TrailingStopLossOrderRejectTransaction,
        )
        from .stop_loss_order_reject_transaction import StopLossOrderRejectTransaction
        from .take_profit_order_reject_transaction import (
            TakeProfitOrderRejectTransaction,
        )
        from .order_cancel_reject_transaction import OrderCancelRejectTransaction

        d = src_dict.copy()
        _take_profit_order_cancel_reject_transaction = d.pop(
            "takeProfitOrderCancelRejectTransaction", None
        )
        take_profit_order_cancel_reject_transaction: Optional[
            OrderCancelRejectTransaction
        ]
        if isinstance(_take_profit_order_cancel_reject_transaction, Unset):
            take_profit_order_cancel_reject_transaction = None
        else:
            take_profit_order_cancel_reject_transaction = (
                OrderCancelRejectTransaction.from_dict(
                    _take_profit_order_cancel_reject_transaction
                )
            )
        _take_profit_order_reject_transaction = d.pop(
            "takeProfitOrderRejectTransaction", None
        )
        take_profit_order_reject_transaction: Optional[TakeProfitOrderRejectTransaction]
        if isinstance(_take_profit_order_reject_transaction, Unset):
            take_profit_order_reject_transaction = None
        else:
            take_profit_order_reject_transaction = (
                TakeProfitOrderRejectTransaction.from_dict(
                    _take_profit_order_reject_transaction
                )
            )
        _stop_loss_order_cancel_reject_transaction = d.pop(
            "stopLossOrderCancelRejectTransaction", None
        )
        stop_loss_order_cancel_reject_transaction: Optional[
            OrderCancelRejectTransaction
        ]
        if isinstance(_stop_loss_order_cancel_reject_transaction, Unset):
            stop_loss_order_cancel_reject_transaction = None
        else:
            stop_loss_order_cancel_reject_transaction = (
                OrderCancelRejectTransaction.from_dict(
                    _stop_loss_order_cancel_reject_transaction
                )
            )
        _stop_loss_order_reject_transaction = d.pop(
            "stopLossOrderRejectTransaction", None
        )
        stop_loss_order_reject_transaction: Optional[StopLossOrderRejectTransaction]
        if isinstance(_stop_loss_order_reject_transaction, Unset):
            stop_loss_order_reject_transaction = None
        else:
            stop_loss_order_reject_transaction = (
                StopLossOrderRejectTransaction.from_dict(
                    _stop_loss_order_reject_transaction
                )
            )
        _trailing_stop_loss_order_cancel_reject_transaction = d.pop(
            "trailingStopLossOrderCancelRejectTransaction", None
        )
        trailing_stop_loss_order_cancel_reject_transaction: Optional[
            OrderCancelRejectTransaction
        ]
        if isinstance(_trailing_stop_loss_order_cancel_reject_transaction, Unset):
            trailing_stop_loss_order_cancel_reject_transaction = None
        else:
            trailing_stop_loss_order_cancel_reject_transaction = (
                OrderCancelRejectTransaction.from_dict(
                    _trailing_stop_loss_order_cancel_reject_transaction
                )
            )
        _trailing_stop_loss_order_reject_transaction = d.pop(
            "trailingStopLossOrderRejectTransaction", None
        )
        trailing_stop_loss_order_reject_transaction: Optional[
            TrailingStopLossOrderRejectTransaction
        ]
        if isinstance(_trailing_stop_loss_order_reject_transaction, Unset):
            trailing_stop_loss_order_reject_transaction = None
        else:
            trailing_stop_loss_order_reject_transaction = (
                TrailingStopLossOrderRejectTransaction.from_dict(
                    _trailing_stop_loss_order_reject_transaction
                )
            )
        last_transaction_id = d.pop("lastTransactionID", None)
        related_transaction_i_ds = cast(List[str], d.pop("relatedTransactionIDs", None))
        error_code = d.pop("errorCode", None)
        error_message = d.pop("errorMessage", None)
        set_trade_dependent_orders_response_400 = cls(
            take_profit_order_cancel_reject_transaction=take_profit_order_cancel_reject_transaction,
            take_profit_order_reject_transaction=take_profit_order_reject_transaction,
            stop_loss_order_cancel_reject_transaction=stop_loss_order_cancel_reject_transaction,
            stop_loss_order_reject_transaction=stop_loss_order_reject_transaction,
            trailing_stop_loss_order_cancel_reject_transaction=trailing_stop_loss_order_cancel_reject_transaction,
            trailing_stop_loss_order_reject_transaction=trailing_stop_loss_order_reject_transaction,
            last_transaction_id=last_transaction_id,
            related_transaction_i_ds=related_transaction_i_ds,
            error_code=error_code,
            error_message=error_message,
        )
        set_trade_dependent_orders_response_400.additional_properties = d
        return set_trade_dependent_orders_response_400

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
