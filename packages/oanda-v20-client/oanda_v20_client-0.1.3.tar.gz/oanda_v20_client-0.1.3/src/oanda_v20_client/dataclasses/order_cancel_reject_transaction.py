from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .order_cancel_reject_transaction_reject_reason import (
    OrderCancelRejectTransactionRejectReason,
)
from .order_cancel_reject_transaction_type import OrderCancelRejectTransactionType
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

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

    id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    account_id: Union[Unset, str] = UNSET
    batch_id: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    type: Union[Unset, OrderCancelRejectTransactionType] = UNSET
    order_id: Union[Unset, str] = UNSET
    client_order_id: Union[Unset, str] = UNSET
    reject_reason: Union[Unset, OrderCancelRejectTransactionRejectReason] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OrderCancelRejectTransaction":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
