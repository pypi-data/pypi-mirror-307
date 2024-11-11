from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from typing import Optional, TypeVar

T = TypeVar("T", bound="ClientExtensions")


@dataclasses.dataclass
class ClientExtensions:
    """A ClientExtensions object allows a client to attach a clientID, tag and comment to Orders and Trades in their
    Account.  Do not set, modify, or delete this field if your account is associated with MT4.

        Attributes:
            id (Union[Unset, str]): The Client ID of the Order/Trade
            tag (Union[Unset, str]): A tag associated with the Order/Trade
            comment (Union[Unset, str]): A comment associated with the Order/Trade"""

    id: Optional[str]
    tag: Optional[str]
    comment: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClientExtensions":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
