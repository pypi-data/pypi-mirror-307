from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .order_cancel_transaction import OrderCancelTransaction
from .order_fill_transaction import OrderFillTransaction
from .transaction import Transaction
from typing import List, TypeVar, Union

T = TypeVar("T", bound="CreateOrderResponse201")


@dataclasses.dataclass
class CreateOrderResponse201:
    """Attributes:
    order_create_transaction (Union[Unset, Transaction]): The base Transaction specification. Specifies properties
        that are common between all Transaction.
    order_fill_transaction (Union[Unset, OrderFillTransaction]): An OrderFillTransaction represents the filling of
        an Order in the client's Account.
    order_cancel_transaction (Union[Unset, OrderCancelTransaction]): An OrderCancelTransaction represents the
        cancellation of an Order in the client's Account.
    order_reissue_transaction (Union[Unset, Transaction]): The base Transaction specification. Specifies properties
        that are common between all Transaction.
    order_reissue_reject_transaction (Union[Unset, Transaction]): The base Transaction specification. Specifies
        properties that are common between all Transaction.
    related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
        satisfying the request.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    order_create_transaction: Union[Unset, "Transaction"] = UNSET
    order_fill_transaction: Union[Unset, "OrderFillTransaction"] = UNSET
    order_cancel_transaction: Union[Unset, "OrderCancelTransaction"] = UNSET
    order_reissue_transaction: Union[Unset, "Transaction"] = UNSET
    order_reissue_reject_transaction: Union[Unset, "Transaction"] = UNSET
    related_transaction_i_ds: Union[Unset, List[str]] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CreateOrderResponse201":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
