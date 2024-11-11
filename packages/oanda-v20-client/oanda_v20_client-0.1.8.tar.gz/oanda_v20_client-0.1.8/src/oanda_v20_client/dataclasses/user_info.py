from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

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

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        username = d.pop("username", None)
        user_id = d.pop("userID", None)
        country = d.pop("country", None)
        email_address = d.pop("emailAddress", None)
        user_info = cls(
            username=username,
            user_id=user_id,
            country=country,
            email_address=email_address,
        )
        user_info.additional_properties = d
        return user_info

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
