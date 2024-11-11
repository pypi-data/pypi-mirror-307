from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .trade import Trade
from types import UNSET, Unset
from typing import TypeVar
from typing import List
from typing import Union

T = TypeVar("T", bound="ListOpenTradesResponse200")


@dataclasses.dataclass
class ListOpenTradesResponse200:
    """Attributes:
    trades (Union[Unset, List['Trade']]): The Account's list of open Trades
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    trades: Union[Unset, List["Trade"]] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ListOpenTradesResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
