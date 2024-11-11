from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .trade import Trade
from typing import List, TypeVar, Union

T = TypeVar("T", bound="ListTradesResponse200")


@dataclasses.dataclass
class ListTradesResponse200:
    """Attributes:
    trades (Union[Unset, List['Trade']]): The list of Trade detail objects
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    trades: Union[Unset, List["Trade"]] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ListTradesResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
