from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .order_cancel_transaction import OrderCancelTransaction
from .order_fill_transaction import OrderFillTransaction
from .transaction import Transaction
from types import Unset
from typing import List, Optional, Type, TypeVar, cast

T = TypeVar("T", bound="ReplaceOrderResponse201")


@dataclasses.dataclass
class ReplaceOrderResponse201:
    """Attributes:
    order_cancel_transaction (Union[Unset, OrderCancelTransaction]): An OrderCancelTransaction represents the
        cancellation of an Order in the client's Account.
    order_create_transaction (Union[Unset, Transaction]): The base Transaction specification. Specifies properties
        that are common between all Transaction.
    order_fill_transaction (Union[Unset, OrderFillTransaction]): An OrderFillTransaction represents the filling of
        an Order in the client's Account.
    order_reissue_transaction (Union[Unset, Transaction]): The base Transaction specification. Specifies properties
        that are common between all Transaction.
    order_reissue_reject_transaction (Union[Unset, Transaction]): The base Transaction specification. Specifies
        properties that are common between all Transaction.
    replacing_order_cancel_transaction (Union[Unset, OrderCancelTransaction]): An OrderCancelTransaction represents
        the cancellation of an Order in the client's Account.
    related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
        satisfying the request.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    order_cancel_transaction: Optional["OrderCancelTransaction"]
    order_create_transaction: Optional["Transaction"]
    order_fill_transaction: Optional["OrderFillTransaction"]
    order_reissue_transaction: Optional["Transaction"]
    order_reissue_reject_transaction: Optional["Transaction"]
    replacing_order_cancel_transaction: Optional["OrderCancelTransaction"]
    related_transaction_i_ds: Optional[List[str]]
    last_transaction_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .order_cancel_transaction import OrderCancelTransaction
        from .transaction import Transaction
        from .order_fill_transaction import OrderFillTransaction

        d = src_dict.copy()
        _order_cancel_transaction = d.pop("orderCancelTransaction", None)
        order_cancel_transaction: Optional[OrderCancelTransaction]
        if isinstance(_order_cancel_transaction, Unset):
            order_cancel_transaction = None
        else:
            order_cancel_transaction = OrderCancelTransaction.from_dict(
                _order_cancel_transaction
            )
        _order_create_transaction = d.pop("orderCreateTransaction", None)
        order_create_transaction: Optional[Transaction]
        if isinstance(_order_create_transaction, Unset):
            order_create_transaction = None
        else:
            order_create_transaction = Transaction.from_dict(_order_create_transaction)
        _order_fill_transaction = d.pop("orderFillTransaction", None)
        order_fill_transaction: Optional[OrderFillTransaction]
        if isinstance(_order_fill_transaction, Unset):
            order_fill_transaction = None
        else:
            order_fill_transaction = OrderFillTransaction.from_dict(
                _order_fill_transaction
            )
        _order_reissue_transaction = d.pop("orderReissueTransaction", None)
        order_reissue_transaction: Optional[Transaction]
        if isinstance(_order_reissue_transaction, Unset):
            order_reissue_transaction = None
        else:
            order_reissue_transaction = Transaction.from_dict(
                _order_reissue_transaction
            )
        _order_reissue_reject_transaction = d.pop("orderReissueRejectTransaction", None)
        order_reissue_reject_transaction: Optional[Transaction]
        if isinstance(_order_reissue_reject_transaction, Unset):
            order_reissue_reject_transaction = None
        else:
            order_reissue_reject_transaction = Transaction.from_dict(
                _order_reissue_reject_transaction
            )
        _replacing_order_cancel_transaction = d.pop(
            "replacingOrderCancelTransaction", None
        )
        replacing_order_cancel_transaction: Optional[OrderCancelTransaction]
        if isinstance(_replacing_order_cancel_transaction, Unset):
            replacing_order_cancel_transaction = None
        else:
            replacing_order_cancel_transaction = OrderCancelTransaction.from_dict(
                _replacing_order_cancel_transaction
            )
        related_transaction_i_ds = cast(List[str], d.pop("relatedTransactionIDs", None))
        last_transaction_id = d.pop("lastTransactionID", None)
        replace_order_response_201 = cls(
            order_cancel_transaction=order_cancel_transaction,
            order_create_transaction=order_create_transaction,
            order_fill_transaction=order_fill_transaction,
            order_reissue_transaction=order_reissue_transaction,
            order_reissue_reject_transaction=order_reissue_reject_transaction,
            replacing_order_cancel_transaction=replacing_order_cancel_transaction,
            related_transaction_i_ds=related_transaction_i_ds,
            last_transaction_id=last_transaction_id,
        )
        replace_order_response_201.additional_properties = d
        return replace_order_response_201

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
