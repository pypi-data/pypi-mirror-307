from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

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

    trade_id: Optional[str]
    client_trade_id: Optional[str]
    source_transaction_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        trade_id = d.pop("tradeID", None)
        client_trade_id = d.pop("clientTradeID", None)
        source_transaction_id = d.pop("sourceTransactionID", None)
        market_order_delayed_trade_close = cls(
            trade_id=trade_id,
            client_trade_id=client_trade_id,
            source_transaction_id=source_transaction_id,
        )
        market_order_delayed_trade_close.additional_properties = d
        return market_order_delayed_trade_close

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
