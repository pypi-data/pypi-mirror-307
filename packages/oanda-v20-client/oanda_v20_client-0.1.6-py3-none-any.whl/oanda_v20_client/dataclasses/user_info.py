from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from typing import Optional, TypeVar

T = TypeVar("T", bound="UserInfo")


@dataclasses.dataclass
class UserInfo:
    """A representation of user information, as provided to the user themself.

    Attributes:
        username (Union[Unset, str]): The user-provided username.
        user_id (Union[Unset, int]): The user's OANDA-assigned user ID.
        country (Union[Unset, str]): The country that the user is based in.
        email_address (Union[Unset, str]): The user's email address."""

    username: Optional[str]
    user_id: Optional[int]
    country: Optional[str]
    email_address: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserInfo":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
