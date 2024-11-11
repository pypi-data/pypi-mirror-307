from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from typing import List, Optional, TypeVar

T = TypeVar("T", bound="AccountProperties")


@dataclasses.dataclass
class AccountProperties:
    """Properties related to an Account.

    Attributes:
        id (Union[Unset, str]): The Account's identifier
        mt_4_account_id (Union[Unset, int]): The Account's associated MT4 Account ID. This field will not be present if
            the Account is not an MT4 account.
        tags (Union[Unset, List[str]]): The Account's tags"""

    id: Optional[str]
    mt_4_account_id: Optional[int]
    tags: Optional[List[str]]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AccountProperties":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
