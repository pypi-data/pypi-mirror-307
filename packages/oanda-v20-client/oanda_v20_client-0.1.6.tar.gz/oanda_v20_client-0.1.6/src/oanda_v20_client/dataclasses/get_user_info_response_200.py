from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .user_info import UserInfo
from typing import Optional, TypeVar

T = TypeVar("T", bound="GetUserInfoResponse200")


@dataclasses.dataclass
class GetUserInfoResponse200:
    """Attributes:
    user_info (Union[Unset, UserInfo]): A representation of user information, as provided to the user themself."""

    user_info: Optional["UserInfo"]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetUserInfoResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
