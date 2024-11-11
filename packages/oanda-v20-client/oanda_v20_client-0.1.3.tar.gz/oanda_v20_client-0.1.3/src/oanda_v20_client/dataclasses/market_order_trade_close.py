from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="MarketOrderTradeClose")


@dataclasses.dataclass
class MarketOrderTradeClose:
    """A MarketOrderTradeClose specifies the extensions to a Market Order that has been created specifically to close a
    Trade.

        Attributes:
            trade_id (Union[Unset, str]): The ID of the Trade requested to be closed
            client_trade_id (Union[Unset, str]): The client ID of the Trade requested to be closed
            units (Union[Unset, str]): Indication of how much of the Trade to close. Either "ALL", or a DecimalNumber
                reflection a partial close of the Trade."""

    trade_id: Union[Unset, str] = UNSET
    client_trade_id: Union[Unset, str] = UNSET
    units: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MarketOrderTradeClose":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
