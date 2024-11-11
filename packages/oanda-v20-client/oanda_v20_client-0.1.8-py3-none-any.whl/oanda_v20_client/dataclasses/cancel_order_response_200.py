from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .order_cancel_transaction import OrderCancelTransaction
from types import Unset
from typing import List, Optional, Type, TypeVar, cast

T = TypeVar("T", bound="CancelOrderResponse200")


@dataclasses.dataclass
class CancelOrderResponse200:
    """Attributes:
    order_cancel_transaction (Union[Unset, OrderCancelTransaction]): An OrderCancelTransaction represents the
        cancellation of an Order in the client's Account.
    related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
        satisfying the request.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    order_cancel_transaction: Optional["OrderCancelTransaction"]
    related_transaction_i_ds: Optional[List[str]]
    last_transaction_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .order_cancel_transaction import OrderCancelTransaction

        d = src_dict.copy()
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
        cancel_order_response_200 = cls(
            order_cancel_transaction=order_cancel_transaction,
            related_transaction_i_ds=related_transaction_i_ds,
            last_transaction_id=last_transaction_id,
        )
        cancel_order_response_200.additional_properties = d
        return cancel_order_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
