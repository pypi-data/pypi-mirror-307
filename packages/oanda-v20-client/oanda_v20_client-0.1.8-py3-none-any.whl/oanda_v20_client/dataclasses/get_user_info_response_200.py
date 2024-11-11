from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .user_info import UserInfo
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="GetUserInfoResponse200")


@dataclasses.dataclass
class GetUserInfoResponse200:
    """Attributes:
    user_info (Union[Unset, UserInfo]): A representation of user information, as provided to the user themself."""

    user_info: Optional["UserInfo"]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .user_info import UserInfo

        d = src_dict.copy()
        _user_info = d.pop("userInfo", None)
        user_info: Optional[UserInfo]
        if isinstance(_user_info, Unset):
            user_info = None
        else:
            user_info = UserInfo.from_dict(_user_info)
        get_user_info_response_200 = cls(user_info=user_info)
        get_user_info_response_200.additional_properties = d
        return get_user_info_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
