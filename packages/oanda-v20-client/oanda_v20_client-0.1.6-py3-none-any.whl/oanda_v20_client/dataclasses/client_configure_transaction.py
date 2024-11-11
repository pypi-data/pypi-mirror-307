from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .client_configure_transaction_type import ClientConfigureTransactionType
from typing import Optional, TypeVar

T = TypeVar("T", bound="ClientConfigureTransaction")


@dataclasses.dataclass
class ClientConfigureTransaction:
    """A ClientConfigureTransaction represents the configuration of an Account by a client.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, ClientConfigureTransactionType]): The Type of the Transaction. Always set to
            "CLIENT_CONFIGURE" in a ClientConfigureTransaction.
        alias (Union[Unset, str]): The client-provided alias for the Account.
        margin_rate (Union[Unset, str]): The margin rate override for the Account."""

    id: Optional[str]
    time: Optional[str]
    user_id: Optional[int]
    account_id: Optional[str]
    batch_id: Optional[str]
    request_id: Optional[str]
    type: Optional[ClientConfigureTransactionType]
    alias: Optional[str]
    margin_rate: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClientConfigureTransaction":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
