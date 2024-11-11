from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

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

    trade_id: Optional[str]
    client_trade_id: Optional[str]
    units: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        trade_id = d.pop("tradeID", None)
        client_trade_id = d.pop("clientTradeID", None)
        units = d.pop("units", None)
        market_order_trade_close = cls(
            trade_id=trade_id, client_trade_id=client_trade_id, units=units
        )
        market_order_trade_close.additional_properties = d
        return market_order_trade_close

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
