from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_configure_reject_transaction_reject_reason import (
    ClientConfigureRejectTransactionRejectReason,
)
from .client_configure_reject_transaction_reject_reason import (
    check_client_configure_reject_transaction_reject_reason,
)
from .client_configure_reject_transaction_type import (
    ClientConfigureRejectTransactionType,
)
from .client_configure_reject_transaction_type import (
    check_client_configure_reject_transaction_type,
)
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="ClientConfigureRejectTransaction")


@dataclasses.dataclass
class ClientConfigureRejectTransaction:
    """A ClientConfigureRejectTransaction represents the reject of configuration of an Account by a client.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, ClientConfigureRejectTransactionType]): The Type of the Transaction. Always set to
            "CLIENT_CONFIGURE_REJECT" in a ClientConfigureRejectTransaction.
        alias (Union[Unset, str]): The client-provided alias for the Account.
        margin_rate (Union[Unset, str]): The margin rate override for the Account.
        reject_reason (Union[Unset, ClientConfigureRejectTransactionRejectReason]): The reason that the Reject
            Transaction was created"""

    id: Optional[str]
    time: Optional[str]
    user_id: Optional[int]
    account_id: Optional[str]
    batch_id: Optional[str]
    request_id: Optional[str]
    type: Optional[ClientConfigureRejectTransactionType]
    alias: Optional[str]
    margin_rate: Optional[str]
    reject_reason: Optional[ClientConfigureRejectTransactionRejectReason]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", None)
        time = d.pop("time", None)
        user_id = d.pop("userID", None)
        account_id = d.pop("accountID", None)
        batch_id = d.pop("batchID", None)
        request_id = d.pop("requestID", None)
        _type = d.pop("type", None)
        type: Optional[ClientConfigureRejectTransactionType]
        if _type is None:
            type = None
        else:
            type = check_client_configure_reject_transaction_type(_type)
        alias = d.pop("alias", None)
        margin_rate = d.pop("marginRate", None)
        _reject_reason = d.pop("rejectReason", None)
        reject_reason: Optional[ClientConfigureRejectTransactionRejectReason]
        if isinstance(_reject_reason, Unset):
            reject_reason = None
        else:
            reject_reason = check_client_configure_reject_transaction_reject_reason(
                _reject_reason
            )
        client_configure_reject_transaction = cls(
            id=id,
            time=time,
            user_id=user_id,
            account_id=account_id,
            batch_id=batch_id,
            request_id=request_id,
            type=type,
            alias=alias,
            margin_rate=margin_rate,
            reject_reason=reject_reason,
        )
        client_configure_reject_transaction.additional_properties = d
        return client_configure_reject_transaction

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
