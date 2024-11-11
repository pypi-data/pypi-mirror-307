from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="TradeReduce")


@dataclasses.dataclass
class TradeReduce:
    """A TradeReduce object represents a Trade for an instrument that was reduced (either partially or fully) in an
    Account. It is found embedded in Transactions that affect the position of an instrument in the account, specifically
    the OrderFill Transaction.

        Attributes:
            trade_id (Union[Unset, str]): The ID of the Trade that was reduced or closed
            units (Union[Unset, str]): The number of units that the Trade was reduced by
            price (Union[Unset, str]): The average price that the units were closed at. This price may be clamped for
                guaranteed Stop Loss Orders.
            realized_pl (Union[Unset, str]): The PL realized when reducing the Trade
            financing (Union[Unset, str]): The financing paid/collected when reducing the Trade
            guaranteed_execution_fee (Union[Unset, str]): This is the fee that is charged for closing the Trade if it has a
                guaranteed Stop Loss Order attached to it.
            half_spread_cost (Union[Unset, str]): The half spread cost for the trade reduce/close. This can be a positive or
                negative value and is represented in the home currency of the Account."""

    trade_id: Union[Unset, str] = UNSET
    units: Union[Unset, str] = UNSET
    price: Union[Unset, str] = UNSET
    realized_pl: Union[Unset, str] = UNSET
    financing: Union[Unset, str] = UNSET
    guaranteed_execution_fee: Union[Unset, str] = UNSET
    half_spread_cost: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TradeReduce":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
