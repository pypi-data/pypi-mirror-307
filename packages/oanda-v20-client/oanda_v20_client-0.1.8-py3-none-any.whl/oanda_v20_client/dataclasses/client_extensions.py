from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

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

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", None)
        tag = d.pop("tag", None)
        comment = d.pop("comment", None)
        client_extensions = cls(id=id, tag=tag, comment=comment)
        client_extensions.additional_properties = d
        return client_extensions

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
