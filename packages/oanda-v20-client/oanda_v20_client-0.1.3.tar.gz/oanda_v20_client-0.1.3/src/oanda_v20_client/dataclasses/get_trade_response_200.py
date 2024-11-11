from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .trade import Trade
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="GetTradeResponse200")


@dataclasses.dataclass
class GetTradeResponse200:
    """Attributes:
    trade (Union[Unset, Trade]): The specification of a Trade within an Account. This includes the full
        representation of the Trade's dependent Orders in addition to the IDs of those Orders.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    trade: Union[Unset, "Trade"] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetTradeResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
