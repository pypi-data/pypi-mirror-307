from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .account import Account
from typing import Optional, TypeVar

T = TypeVar("T", bound="GetAccountResponse200")


@dataclasses.dataclass
class GetAccountResponse200:
    """Attributes:
    account (Union[Unset, Account]): The full details of a client's Account. This includes full open Trade, open
        Position and pending Order representation.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account."""

    account: Optional["Account"]
    last_transaction_id: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetAccountResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
