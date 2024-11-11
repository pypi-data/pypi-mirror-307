from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .account_summary import AccountSummary
from typing import Optional, TypeVar

T = TypeVar("T", bound="GetAccountSummaryResponse200")


@dataclasses.dataclass
class GetAccountSummaryResponse200:
    """Attributes:
    account (Union[Unset, AccountSummary]): A summary representation of a client's Account. The AccountSummary does
        not provide to full specification of pending Orders, open Trades and Positions.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account."""

    account: Optional["AccountSummary"]
    last_transaction_id: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetAccountSummaryResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
