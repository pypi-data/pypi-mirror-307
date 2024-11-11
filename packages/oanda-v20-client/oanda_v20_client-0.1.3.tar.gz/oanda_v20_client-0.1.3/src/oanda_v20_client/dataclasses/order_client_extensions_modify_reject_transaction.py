from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .client_extensions import ClientExtensions
from .order_client_extensions_modify_reject_transaction_reject_reason import (
    OrderClientExtensionsModifyRejectTransactionRejectReason,
)
from .order_client_extensions_modify_reject_transaction_type import (
    OrderClientExtensionsModifyRejectTransactionType,
)
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="OrderClientExtensionsModifyRejectTransaction")


@dataclasses.dataclass
class OrderClientExtensionsModifyRejectTransaction:
    """A OrderClientExtensionsModifyRejectTransaction represents the rejection of the modification of an Order's Client
    Extensions.

        Attributes:
            id (Union[Unset, str]): The Transaction's Identifier.
            time (Union[Unset, str]): The date/time when the Transaction was created.
            user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
            account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
            batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
                batch are applied to the Account simultaneously.
            request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
            type (Union[Unset, OrderClientExtensionsModifyRejectTransactionType]): The Type of the Transaction. Always set
                to "ORDER_CLIENT_EXTENSIONS_MODIFY_REJECT" for a OrderClientExtensionsModifyRejectTransaction.
            order_id (Union[Unset, str]): The ID of the Order who's client extensions are to be modified.
            client_order_id (Union[Unset, str]): The original Client ID of the Order who's client extensions are to be
                modified.
            client_extensions_modify (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
                clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
                your account is associated with MT4.
            trade_client_extensions_modify (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to
                attach a clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this
                field if your account is associated with MT4.
            reject_reason (Union[Unset, OrderClientExtensionsModifyRejectTransactionRejectReason]): The reason that the
                Reject Transaction was created"""

    id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    account_id: Union[Unset, str] = UNSET
    batch_id: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    type: Union[Unset, OrderClientExtensionsModifyRejectTransactionType] = UNSET
    order_id: Union[Unset, str] = UNSET
    client_order_id: Union[Unset, str] = UNSET
    client_extensions_modify: Union[Unset, "ClientExtensions"] = UNSET
    trade_client_extensions_modify: Union[Unset, "ClientExtensions"] = UNSET
    reject_reason: Union[
        Unset, OrderClientExtensionsModifyRejectTransactionRejectReason
    ] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any]
    ) -> "OrderClientExtensionsModifyRejectTransaction":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
