from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .order_cancel_transaction import OrderCancelTransaction
from .order_fill_transaction import OrderFillTransaction
from .transaction import Transaction
from typing import List, Optional, TypeVar

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

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReplaceOrderResponse201":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
