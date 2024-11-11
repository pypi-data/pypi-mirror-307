from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .trade import Trade
from typing import List, Optional, TypeVar

T = TypeVar("T", bound="ListTradesResponse200")


@dataclasses.dataclass
class ListTradesResponse200:
    """Attributes:
    trades (Union[Unset, List['Trade']]): The list of Trade detail objects
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    trades: Optional[List["Trade"]]
    last_transaction_id: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ListTradesResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
