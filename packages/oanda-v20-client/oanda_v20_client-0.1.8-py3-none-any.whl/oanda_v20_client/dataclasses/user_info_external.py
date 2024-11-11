from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="UserInfoExternal")


@dataclasses.dataclass
class UserInfoExternal:
    """A representation of user information, as available to external (3rd party) clients.

    Attributes:
        user_id (Union[Unset, int]): The user's OANDA-assigned user ID.
        country (Union[Unset, str]): The country that the user is based in.
        fifo (Union[Unset, bool]): Flag indicating if the the user's Accounts adhere to FIFO execution rules."""

    user_id: Optional[int]
    country: Optional[str]
    fifo: Optional[bool]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_id = d.pop("userID", None)
        country = d.pop("country", None)
        fifo = d.pop("FIFO", None)
        user_info_external = cls(user_id=user_id, country=country, fifo=fifo)
        user_info_external.additional_properties = d
        return user_info_external

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
