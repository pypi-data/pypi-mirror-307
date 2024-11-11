from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .user_info_external import UserInfoExternal
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="GetExternalUserInfoResponse200")


@dataclasses.dataclass
class GetExternalUserInfoResponse200:
    """Attributes:
    user_info (Union[Unset, UserInfoExternal]): A representation of user information, as available to external (3rd
        party) clients."""

    user_info: Optional["UserInfoExternal"]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .user_info_external import UserInfoExternal

        d = src_dict.copy()
        _user_info = d.pop("userInfo", None)
        user_info: Optional[UserInfoExternal]
        if isinstance(_user_info, Unset):
            user_info = None
        else:
            user_info = UserInfoExternal.from_dict(_user_info)
        get_external_user_info_response_200 = cls(user_info=user_info)
        get_external_user_info_response_200.additional_properties = d
        return get_external_user_info_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
