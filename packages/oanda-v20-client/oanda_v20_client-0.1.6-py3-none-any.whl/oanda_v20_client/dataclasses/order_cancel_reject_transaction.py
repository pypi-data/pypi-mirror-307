from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .order_cancel_reject_transaction_reject_reason import (
    OrderCancelRejectTransactionRejectReason,
)
from .order_cancel_reject_transaction_type import OrderCancelRejectTransactionType
from typing import Optional, TypeVar

T = TypeVar("T", bound="OrderCancelRejectTransaction")


@dataclasses.dataclass
class OrderCancelRejectTransaction:
    """An OrderCancelRejectTransaction represents the rejection of the cancellation of an Order in the client's Account.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, OrderCancelRejectTransactionType]): The Type of the Transaction. Always set to
            "ORDER_CANCEL_REJECT" for an OrderCancelRejectTransaction.
        order_id (Union[Unset, str]): The ID of the Order intended to be cancelled
        client_order_id (Union[Unset, str]): The client ID of the Order intended to be cancelled (only provided if the
            Order has a client Order ID).
        reject_reason (Union[Unset, OrderCancelRejectTransactionRejectReason]): The reason that the Reject Transaction
            was created"""

    id: Optional[str]
    time: Optional[str]
    user_id: Optional[int]
    account_id: Optional[str]
    batch_id: Optional[str]
    request_id: Optional[str]
    type: Optional[OrderCancelRejectTransactionType]
    order_id: Optional[str]
    client_order_id: Optional[str]
    reject_reason: Optional[OrderCancelRejectTransactionRejectReason]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OrderCancelRejectTransaction":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
