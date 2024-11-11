from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_configure_transaction import ClientConfigureTransaction
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="ConfigureAccountResponse200")


@dataclasses.dataclass
class ConfigureAccountResponse200:
    """Attributes:
    client_configure_transaction (Union[Unset, ClientConfigureTransaction]): A ClientConfigureTransaction represents
        the configuration of an Account by a client.
    last_transaction_id (Union[Unset, str]): The ID of the last Transaction created for the Account."""

    client_configure_transaction: Optional["ClientConfigureTransaction"]
    last_transaction_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .client_configure_transaction import ClientConfigureTransaction

        d = src_dict.copy()
        _client_configure_transaction = d.pop("clientConfigureTransaction", None)
        client_configure_transaction: Optional[ClientConfigureTransaction]
        if isinstance(_client_configure_transaction, Unset):
            client_configure_transaction = None
        else:
            client_configure_transaction = ClientConfigureTransaction.from_dict(
                _client_configure_transaction
            )
        last_transaction_id = d.pop("lastTransactionID", None)
        configure_account_response_200 = cls(
            client_configure_transaction=client_configure_transaction,
            last_transaction_id=last_transaction_id,
        )
        configure_account_response_200.additional_properties = d
        return configure_account_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
