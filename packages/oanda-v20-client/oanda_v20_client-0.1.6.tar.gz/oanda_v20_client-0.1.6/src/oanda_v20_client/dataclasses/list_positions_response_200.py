from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .position import Position
from typing import List, Optional, TypeVar

T = TypeVar("T", bound="ListPositionsResponse200")


@dataclasses.dataclass
class ListPositionsResponse200:
    """Attributes:
    positions (Union[Unset, List['Position']]): The list of Account Positions.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    positions: Optional[List["Position"]]
    last_transaction_id: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ListPositionsResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
