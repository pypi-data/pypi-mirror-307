from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .trade import Trade
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="GetTradeResponse200")


@dataclasses.dataclass
class GetTradeResponse200:
    """Attributes:
    trade (Union[Unset, Trade]): The specification of a Trade within an Account. This includes the full
        representation of the Trade's dependent Orders in addition to the IDs of those Orders.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    trade: Optional["Trade"]
    last_transaction_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .trade import Trade

        d = src_dict.copy()
        _trade = d.pop("trade", None)
        trade: Optional[Trade]
        if isinstance(_trade, Unset):
            trade = None
        else:
            trade = Trade.from_dict(_trade)
        last_transaction_id = d.pop("lastTransactionID", None)
        get_trade_response_200 = cls(
            trade=trade, last_transaction_id=last_transaction_id
        )
        get_trade_response_200.additional_properties = d
        return get_trade_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
