from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .order_cancel_transaction_reason import OrderCancelTransactionReason
from .order_cancel_transaction_type import OrderCancelTransactionType
from typing import TypeVar, Union

T = TypeVar("T", bound="OrderCancelTransaction")


@dataclasses.dataclass
class OrderCancelTransaction:
    """An OrderCancelTransaction represents the cancellation of an Order in the client's Account.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, OrderCancelTransactionType]): The Type of the Transaction. Always set to "ORDER_CANCEL" for
            an OrderCancelTransaction.
        order_id (Union[Unset, str]): The ID of the Order cancelled
        client_order_id (Union[Unset, str]): The client ID of the Order cancelled (only provided if the Order has a
            client Order ID).
        reason (Union[Unset, OrderCancelTransactionReason]): The reason that the Order was cancelled.
        replaced_by_order_id (Union[Unset, str]): The ID of the Order that replaced this Order (only provided if this
            Order was cancelled for replacement)."""

    id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    account_id: Union[Unset, str] = UNSET
    batch_id: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    type: Union[Unset, OrderCancelTransactionType] = UNSET
    order_id: Union[Unset, str] = UNSET
    client_order_id: Union[Unset, str] = UNSET
    reason: Union[Unset, OrderCancelTransactionReason] = UNSET
    replaced_by_order_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OrderCancelTransaction":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
