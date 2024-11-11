from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .market_order_transaction import MarketOrderTransaction
from .order_cancel_transaction import OrderCancelTransaction
from .order_fill_transaction import OrderFillTransaction
from types import Unset
from typing import List, Optional, Type, TypeVar, cast

T = TypeVar("T", bound="CloseTradeResponse200")


@dataclasses.dataclass
class CloseTradeResponse200:
    """Attributes:
    order_create_transaction (Union[Unset, MarketOrderTransaction]): A MarketOrderTransaction represents the
        creation of a Market Order in the user's account. A Market Order is an Order that is filled immediately at the
        current market price.
        Market Orders can be specialized when they are created to accomplish a specific task: to close a Trade, to
        closeout a Position or to particiate in in a Margin closeout.
    order_fill_transaction (Union[Unset, OrderFillTransaction]): An OrderFillTransaction represents the filling of
        an Order in the client's Account.
    order_cancel_transaction (Union[Unset, OrderCancelTransaction]): An OrderCancelTransaction represents the
        cancellation of an Order in the client's Account.
    related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
        satisfying the request.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    order_create_transaction: Optional["MarketOrderTransaction"]
    order_fill_transaction: Optional["OrderFillTransaction"]
    order_cancel_transaction: Optional["OrderCancelTransaction"]
    related_transaction_i_ds: Optional[List[str]]
    last_transaction_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .order_cancel_transaction import OrderCancelTransaction
        from .market_order_transaction import MarketOrderTransaction
        from .order_fill_transaction import OrderFillTransaction

        d = src_dict.copy()
        _order_create_transaction = d.pop("orderCreateTransaction", None)
        order_create_transaction: Optional[MarketOrderTransaction]
        if isinstance(_order_create_transaction, Unset):
            order_create_transaction = None
        else:
            order_create_transaction = MarketOrderTransaction.from_dict(
                _order_create_transaction
            )
        _order_fill_transaction = d.pop("orderFillTransaction", None)
        order_fill_transaction: Optional[OrderFillTransaction]
        if isinstance(_order_fill_transaction, Unset):
            order_fill_transaction = None
        else:
            order_fill_transaction = OrderFillTransaction.from_dict(
                _order_fill_transaction
            )
        _order_cancel_transaction = d.pop("orderCancelTransaction", None)
        order_cancel_transaction: Optional[OrderCancelTransaction]
        if isinstance(_order_cancel_transaction, Unset):
            order_cancel_transaction = None
        else:
            order_cancel_transaction = OrderCancelTransaction.from_dict(
                _order_cancel_transaction
            )
        related_transaction_i_ds = cast(List[str], d.pop("relatedTransactionIDs", None))
        last_transaction_id = d.pop("lastTransactionID", None)
        close_trade_response_200 = cls(
            order_create_transaction=order_create_transaction,
            order_fill_transaction=order_fill_transaction,
            order_cancel_transaction=order_cancel_transaction,
            related_transaction_i_ds=related_transaction_i_ds,
            last_transaction_id=last_transaction_id,
        )
        close_trade_response_200.additional_properties = d
        return close_trade_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
