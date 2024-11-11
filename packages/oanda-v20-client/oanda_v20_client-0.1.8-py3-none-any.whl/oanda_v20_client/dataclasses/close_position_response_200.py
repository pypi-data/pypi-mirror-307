from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .market_order_transaction import MarketOrderTransaction
from .order_cancel_transaction import OrderCancelTransaction
from .order_fill_transaction import OrderFillTransaction
from types import Unset
from typing import List, Optional, Type, TypeVar, cast

T = TypeVar("T", bound="ClosePositionResponse200")


@dataclasses.dataclass
class ClosePositionResponse200:
    """Attributes:
    long_order_create_transaction (Union[Unset, MarketOrderTransaction]): A MarketOrderTransaction represents the
        creation of a Market Order in the user's account. A Market Order is an Order that is filled immediately at the
        current market price.
        Market Orders can be specialized when they are created to accomplish a specific task: to close a Trade, to
        closeout a Position or to particiate in in a Margin closeout.
    long_order_fill_transaction (Union[Unset, OrderFillTransaction]): An OrderFillTransaction represents the filling
        of an Order in the client's Account.
    long_order_cancel_transaction (Union[Unset, OrderCancelTransaction]): An OrderCancelTransaction represents the
        cancellation of an Order in the client's Account.
    short_order_create_transaction (Union[Unset, MarketOrderTransaction]): A MarketOrderTransaction represents the
        creation of a Market Order in the user's account. A Market Order is an Order that is filled immediately at the
        current market price.
        Market Orders can be specialized when they are created to accomplish a specific task: to close a Trade, to
        closeout a Position or to particiate in in a Margin closeout.
    short_order_fill_transaction (Union[Unset, OrderFillTransaction]): An OrderFillTransaction represents the
        filling of an Order in the client's Account.
    short_order_cancel_transaction (Union[Unset, OrderCancelTransaction]): An OrderCancelTransaction represents the
        cancellation of an Order in the client's Account.
    related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
        satisfying the request.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    long_order_create_transaction: Optional["MarketOrderTransaction"]
    long_order_fill_transaction: Optional["OrderFillTransaction"]
    long_order_cancel_transaction: Optional["OrderCancelTransaction"]
    short_order_create_transaction: Optional["MarketOrderTransaction"]
    short_order_fill_transaction: Optional["OrderFillTransaction"]
    short_order_cancel_transaction: Optional["OrderCancelTransaction"]
    related_transaction_i_ds: Optional[List[str]]
    last_transaction_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .order_cancel_transaction import OrderCancelTransaction
        from .market_order_transaction import MarketOrderTransaction
        from .order_fill_transaction import OrderFillTransaction

        d = src_dict.copy()
        _long_order_create_transaction = d.pop("longOrderCreateTransaction", None)
        long_order_create_transaction: Optional[MarketOrderTransaction]
        if isinstance(_long_order_create_transaction, Unset):
            long_order_create_transaction = None
        else:
            long_order_create_transaction = MarketOrderTransaction.from_dict(
                _long_order_create_transaction
            )
        _long_order_fill_transaction = d.pop("longOrderFillTransaction", None)
        long_order_fill_transaction: Optional[OrderFillTransaction]
        if isinstance(_long_order_fill_transaction, Unset):
            long_order_fill_transaction = None
        else:
            long_order_fill_transaction = OrderFillTransaction.from_dict(
                _long_order_fill_transaction
            )
        _long_order_cancel_transaction = d.pop("longOrderCancelTransaction", None)
        long_order_cancel_transaction: Optional[OrderCancelTransaction]
        if isinstance(_long_order_cancel_transaction, Unset):
            long_order_cancel_transaction = None
        else:
            long_order_cancel_transaction = OrderCancelTransaction.from_dict(
                _long_order_cancel_transaction
            )
        _short_order_create_transaction = d.pop("shortOrderCreateTransaction", None)
        short_order_create_transaction: Optional[MarketOrderTransaction]
        if isinstance(_short_order_create_transaction, Unset):
            short_order_create_transaction = None
        else:
            short_order_create_transaction = MarketOrderTransaction.from_dict(
                _short_order_create_transaction
            )
        _short_order_fill_transaction = d.pop("shortOrderFillTransaction", None)
        short_order_fill_transaction: Optional[OrderFillTransaction]
        if isinstance(_short_order_fill_transaction, Unset):
            short_order_fill_transaction = None
        else:
            short_order_fill_transaction = OrderFillTransaction.from_dict(
                _short_order_fill_transaction
            )
        _short_order_cancel_transaction = d.pop("shortOrderCancelTransaction", None)
        short_order_cancel_transaction: Optional[OrderCancelTransaction]
        if isinstance(_short_order_cancel_transaction, Unset):
            short_order_cancel_transaction = None
        else:
            short_order_cancel_transaction = OrderCancelTransaction.from_dict(
                _short_order_cancel_transaction
            )
        related_transaction_i_ds = cast(List[str], d.pop("relatedTransactionIDs", None))
        last_transaction_id = d.pop("lastTransactionID", None)
        close_position_response_200 = cls(
            long_order_create_transaction=long_order_create_transaction,
            long_order_fill_transaction=long_order_fill_transaction,
            long_order_cancel_transaction=long_order_cancel_transaction,
            short_order_create_transaction=short_order_create_transaction,
            short_order_fill_transaction=short_order_fill_transaction,
            short_order_cancel_transaction=short_order_cancel_transaction,
            related_transaction_i_ds=related_transaction_i_ds,
            last_transaction_id=last_transaction_id,
        )
        close_position_response_200.additional_properties = d
        return close_position_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
