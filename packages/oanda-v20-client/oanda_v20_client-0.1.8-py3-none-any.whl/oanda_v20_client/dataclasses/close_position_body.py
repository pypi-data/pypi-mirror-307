from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_extensions import ClientExtensions
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="ClosePositionBody")


@dataclasses.dataclass
class ClosePositionBody:
    """Attributes:
    long_units (Union[Unset, str]): Indication of how much of the long Position to closeout. Either the string
        "ALL", the string "NONE", or a DecimalNumber representing how many units of the long position to close using a
        PositionCloseout MarketOrder. The units specified must always be positive.
    long_client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
        clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
        your account is associated with MT4.
    short_units (Union[Unset, str]): Indication of how much of the short Position to closeout. Either the string
        "ALL", the string "NONE", or a DecimalNumber representing how many units of the short position to close using a
        PositionCloseout MarketOrder. The units specified must always be positive.
    short_client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
        clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
        your account is associated with MT4."""

    long_units: Optional[str]
    long_client_extensions: Optional["ClientExtensions"]
    short_units: Optional[str]
    short_client_extensions: Optional["ClientExtensions"]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .client_extensions import ClientExtensions

        d = src_dict.copy()
        long_units = d.pop("longUnits", None)
        _long_client_extensions = d.pop("longClientExtensions", None)
        long_client_extensions: Optional[ClientExtensions]
        if isinstance(_long_client_extensions, Unset):
            long_client_extensions = None
        else:
            long_client_extensions = ClientExtensions.from_dict(_long_client_extensions)
        short_units = d.pop("shortUnits", None)
        _short_client_extensions = d.pop("shortClientExtensions", None)
        short_client_extensions: Optional[ClientExtensions]
        if isinstance(_short_client_extensions, Unset):
            short_client_extensions = None
        else:
            short_client_extensions = ClientExtensions.from_dict(
                _short_client_extensions
            )
        close_position_body = cls(
            long_units=long_units,
            long_client_extensions=long_client_extensions,
            short_units=short_units,
            short_client_extensions=short_client_extensions,
        )
        close_position_body.additional_properties = d
        return close_position_body

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
