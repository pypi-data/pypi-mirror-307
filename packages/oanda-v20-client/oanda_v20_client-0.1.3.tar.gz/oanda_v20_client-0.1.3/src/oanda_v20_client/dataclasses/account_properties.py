from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from types import UNSET, Unset
from typing import TypeVar
from typing import List
from typing import Union

T = TypeVar("T", bound="AccountProperties")


@dataclasses.dataclass
class AccountProperties:
    """Properties related to an Account.

    Attributes:
        id (Union[Unset, str]): The Account's identifier
        mt_4_account_id (Union[Unset, int]): The Account's associated MT4 Account ID. This field will not be present if
            the Account is not an MT4 account.
        tags (Union[Unset, List[str]]): The Account's tags"""

    id: Union[Unset, str] = UNSET
    mt_4_account_id: Union[Unset, int] = UNSET
    tags: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AccountProperties":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
