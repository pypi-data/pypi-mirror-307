from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .client_configure_transaction import ClientConfigureTransaction
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="ConfigureAccountResponse200")


@dataclasses.dataclass
class ConfigureAccountResponse200:
    """Attributes:
    client_configure_transaction (Union[Unset, ClientConfigureTransaction]): A ClientConfigureTransaction represents
        the configuration of an Account by a client.
    last_transaction_id (Union[Unset, str]): The ID of the last Transaction created for the Account."""

    client_configure_transaction: Union[Unset, "ClientConfigureTransaction"] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConfigureAccountResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
