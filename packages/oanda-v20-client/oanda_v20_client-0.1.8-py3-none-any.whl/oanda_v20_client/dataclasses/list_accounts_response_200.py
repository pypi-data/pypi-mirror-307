from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .account_properties import AccountProperties
from typing import List, Optional, Type, TypeVar

T = TypeVar("T", bound="ListAccountsResponse200")


@dataclasses.dataclass
class ListAccountsResponse200:
    """Attributes:
    accounts (Union[Unset, List['AccountProperties']]): The list of Accounts the client is authorized to access and
        their associated properties."""

    accounts: Optional[List["AccountProperties"]]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .account_properties import AccountProperties

        d = src_dict.copy()
        accounts = []
        _accounts = d.pop("accounts", None)
        for accounts_item_data in _accounts or []:
            accounts_item = AccountProperties.from_dict(accounts_item_data)
            accounts.append(accounts_item)
        list_accounts_response_200 = cls(accounts=accounts)
        list_accounts_response_200.additional_properties = d
        return list_accounts_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
