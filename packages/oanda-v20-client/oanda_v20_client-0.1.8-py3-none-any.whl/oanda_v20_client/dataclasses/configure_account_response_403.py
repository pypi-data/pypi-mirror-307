from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_configure_reject_transaction import ClientConfigureRejectTransaction
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="ConfigureAccountResponse403")


@dataclasses.dataclass
class ConfigureAccountResponse403:
    """Attributes:
    client_configure_reject_transaction (Union[Unset, ClientConfigureRejectTransaction]): A
        ClientConfigureRejectTransaction represents the reject of configuration of an Account by a client.
    last_transaction_id (Union[Unset, str]): The ID of the last Transaction created for the Account.
    error_code (Union[Unset, str]): The code of the error that has occurred. This field may not be returned for some
        errors.
    error_message (Union[Unset, str]): The human-readable description of the error that has occurred."""

    client_configure_reject_transaction: Optional["ClientConfigureRejectTransaction"]
    last_transaction_id: Optional[str]
    error_code: Optional[str]
    error_message: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .client_configure_reject_transaction import (
            ClientConfigureRejectTransaction,
        )

        d = src_dict.copy()
        _client_configure_reject_transaction = d.pop(
            "clientConfigureRejectTransaction", None
        )
        client_configure_reject_transaction: Optional[ClientConfigureRejectTransaction]
        if isinstance(_client_configure_reject_transaction, Unset):
            client_configure_reject_transaction = None
        else:
            client_configure_reject_transaction = (
                ClientConfigureRejectTransaction.from_dict(
                    _client_configure_reject_transaction
                )
            )
        last_transaction_id = d.pop("lastTransactionID", None)
        error_code = d.pop("errorCode", None)
        error_message = d.pop("errorMessage", None)
        configure_account_response_403 = cls(
            client_configure_reject_transaction=client_configure_reject_transaction,
            last_transaction_id=last_transaction_id,
            error_code=error_code,
            error_message=error_message,
        )
        configure_account_response_403.additional_properties = d
        return configure_account_response_403

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
