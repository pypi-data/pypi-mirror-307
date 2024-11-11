from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .client_extensions import ClientExtensions
from typing import Optional, TypeVar

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

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClosePositionBody":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
