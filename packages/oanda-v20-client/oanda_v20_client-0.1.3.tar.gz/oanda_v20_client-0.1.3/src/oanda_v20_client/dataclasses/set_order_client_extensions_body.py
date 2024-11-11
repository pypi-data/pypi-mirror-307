from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .client_extensions import ClientExtensions
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="SetOrderClientExtensionsBody")


@dataclasses.dataclass
class SetOrderClientExtensionsBody:
    """Attributes:
    client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
        clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
        your account is associated with MT4.
    trade_client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
        clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
        your account is associated with MT4."""

    client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    trade_client_extensions: Union[Unset, "ClientExtensions"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SetOrderClientExtensionsBody":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
