from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="MarketOrderDelayedTradeClose")


@dataclasses.dataclass
class MarketOrderDelayedTradeClose:
    """Details for the Market Order extensions specific to a Market Order placed with the intent of fully closing a
    specific open trade that should have already been closed but wasn't due to halted market conditions

        Attributes:
            trade_id (Union[Unset, str]): The ID of the Trade being closed
            client_trade_id (Union[Unset, str]): The Client ID of the Trade being closed
            source_transaction_id (Union[Unset, str]): The Transaction ID of the DelayedTradeClosure transaction to which
                this Delayed Trade Close belongs to"""

    trade_id: Union[Unset, str] = UNSET
    client_trade_id: Union[Unset, str] = UNSET
    source_transaction_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MarketOrderDelayedTradeClose":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
