from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .trade import Trade
from typing import List, Optional, Type, TypeVar

T = TypeVar("T", bound="ListTradesResponse200")


@dataclasses.dataclass
class ListTradesResponse200:
    """Attributes:
    trades (Union[Unset, List['Trade']]): The list of Trade detail objects
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    trades: Optional[List["Trade"]]
    last_transaction_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .trade import Trade

        d = src_dict.copy()
        trades = []
        _trades = d.pop("trades", None)
        for trades_item_data in _trades or []:
            trades_item = Trade.from_dict(trades_item_data)
            trades.append(trades_item)
        last_transaction_id = d.pop("lastTransactionID", None)
        list_trades_response_200 = cls(
            trades=trades, last_transaction_id=last_transaction_id
        )
        list_trades_response_200.additional_properties = d
        return list_trades_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
