from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import List, Optional, Type, TypeVar, cast

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

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", None)
        mt_4_account_id = d.pop("mt4AccountID", None)
        tags = cast(List[str], d.pop("tags", None))
        account_properties = cls(id=id, mt_4_account_id=mt_4_account_id, tags=tags)
        account_properties.additional_properties = d
        return account_properties

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
