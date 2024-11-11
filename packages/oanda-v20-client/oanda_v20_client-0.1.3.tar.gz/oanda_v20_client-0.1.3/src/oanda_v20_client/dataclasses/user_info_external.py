from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="UserInfoExternal")


@dataclasses.dataclass
class UserInfoExternal:
    """A representation of user information, as available to external (3rd party) clients.

    Attributes:
        user_id (Union[Unset, int]): The user's OANDA-assigned user ID.
        country (Union[Unset, str]): The country that the user is based in.
        fifo (Union[Unset, bool]): Flag indicating if the the user's Accounts adhere to FIFO execution rules."""

    user_id: Union[Unset, int] = UNSET
    country: Union[Unset, str] = UNSET
    fifo: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserInfoExternal":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
