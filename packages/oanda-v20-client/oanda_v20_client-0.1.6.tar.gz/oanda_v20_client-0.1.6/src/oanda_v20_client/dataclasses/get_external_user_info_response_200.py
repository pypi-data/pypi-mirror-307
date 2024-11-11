from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .user_info_external import UserInfoExternal
from typing import Optional, TypeVar

T = TypeVar("T", bound="GetExternalUserInfoResponse200")


@dataclasses.dataclass
class GetExternalUserInfoResponse200:
    """Attributes:
    user_info (Union[Unset, UserInfoExternal]): A representation of user information, as available to external (3rd
        party) clients."""

    user_info: Optional["UserInfoExternal"]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetExternalUserInfoResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
