from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .client_configure_reject_transaction import ClientConfigureRejectTransaction
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="ConfigureAccountResponse400")


@dataclasses.dataclass
class ConfigureAccountResponse400:
    """Attributes:
    client_configure_reject_transaction (Union[Unset, ClientConfigureRejectTransaction]): A
        ClientConfigureRejectTransaction represents the reject of configuration of an Account by a client.
    last_transaction_id (Union[Unset, str]): The ID of the last Transaction created for the Account.
    error_code (Union[Unset, str]): The code of the error that has occurred. This field may not be returned for some
        errors.
    error_message (Union[Unset, str]): The human-readable description of the error that has occurred."""

    client_configure_reject_transaction: Union[
        Unset, "ClientConfigureRejectTransaction"
    ] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    error_code: Union[Unset, str] = UNSET
    error_message: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConfigureAccountResponse400":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
