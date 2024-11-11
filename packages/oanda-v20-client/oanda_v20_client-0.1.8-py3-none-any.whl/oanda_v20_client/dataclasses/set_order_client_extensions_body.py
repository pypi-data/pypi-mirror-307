from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_extensions import ClientExtensions
from types import Unset
from typing import Optional, Type, TypeVar

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

    client_extensions: Optional["ClientExtensions"]
    trade_client_extensions: Optional["ClientExtensions"]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .client_extensions import ClientExtensions

        d = src_dict.copy()
        _client_extensions = d.pop("clientExtensions", None)
        client_extensions: Optional[ClientExtensions]
        if isinstance(_client_extensions, Unset):
            client_extensions = None
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)
        _trade_client_extensions = d.pop("tradeClientExtensions", None)
        trade_client_extensions: Optional[ClientExtensions]
        if isinstance(_trade_client_extensions, Unset):
            trade_client_extensions = None
        else:
            trade_client_extensions = ClientExtensions.from_dict(
                _trade_client_extensions
            )
        set_order_client_extensions_body = cls(
            client_extensions=client_extensions,
            trade_client_extensions=trade_client_extensions,
        )
        set_order_client_extensions_body.additional_properties = d
        return set_order_client_extensions_body

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
