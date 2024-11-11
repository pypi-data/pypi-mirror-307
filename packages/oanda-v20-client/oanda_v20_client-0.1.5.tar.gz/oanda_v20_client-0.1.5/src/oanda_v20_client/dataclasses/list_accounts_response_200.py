from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .account_properties import AccountProperties
from typing import List, TypeVar, Union

T = TypeVar("T", bound="ListAccountsResponse200")


@dataclasses.dataclass
class ListAccountsResponse200:
    """Attributes:
    accounts (Union[Unset, List['AccountProperties']]): The list of Accounts the client is authorized to access and
        their associated properties."""

    accounts: Union[Unset, List["AccountProperties"]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ListAccountsResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
