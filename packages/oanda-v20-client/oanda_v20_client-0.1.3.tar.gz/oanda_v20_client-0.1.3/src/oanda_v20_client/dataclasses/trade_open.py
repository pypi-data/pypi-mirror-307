from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .client_extensions import ClientExtensions
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="TradeOpen")


@dataclasses.dataclass
class TradeOpen:
    """A TradeOpen object represents a Trade for an instrument that was opened in an Account. It is found embedded in
    Transactions that affect the position of an instrument in the Account, specifically the OrderFill Transaction.

        Attributes:
            trade_id (Union[Unset, str]): The ID of the Trade that was opened
            units (Union[Unset, str]): The number of units opened by the Trade
            price (Union[Unset, str]): The average price that the units were opened at.
            guaranteed_execution_fee (Union[Unset, str]): This is the fee charged for opening the trade if it has a
                guaranteed Stop Loss Order attached to it.
            client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
                clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
                your account is associated with MT4.
            half_spread_cost (Union[Unset, str]): The half spread cost for the trade open. This can be a positive or
                negative value and is represented in the home currency of the Account.
            initial_margin_required (Union[Unset, str]): The margin required at the time the Trade was created. Note, this
                is the 'pure' margin required, it is not the 'effective' margin used that factors in the trade risk if a GSLO is
                attached to the trade."""

    trade_id: Union[Unset, str] = UNSET
    units: Union[Unset, str] = UNSET
    price: Union[Unset, str] = UNSET
    guaranteed_execution_fee: Union[Unset, str] = UNSET
    client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    half_spread_cost: Union[Unset, str] = UNSET
    initial_margin_required: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TradeOpen":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
