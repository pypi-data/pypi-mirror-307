from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_extensions import ClientExtensions
from types import Unset
from typing import Optional, Type, TypeVar

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

    trade_id: Optional[str]
    units: Optional[str]
    price: Optional[str]
    guaranteed_execution_fee: Optional[str]
    client_extensions: Optional["ClientExtensions"]
    half_spread_cost: Optional[str]
    initial_margin_required: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .client_extensions import ClientExtensions

        d = src_dict.copy()
        trade_id = d.pop("tradeID", None)
        units = d.pop("units", None)
        price = d.pop("price", None)
        guaranteed_execution_fee = d.pop("guaranteedExecutionFee", None)
        _client_extensions = d.pop("clientExtensions", None)
        client_extensions: Optional[ClientExtensions]
        if isinstance(_client_extensions, Unset):
            client_extensions = None
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)
        half_spread_cost = d.pop("halfSpreadCost", None)
        initial_margin_required = d.pop("initialMarginRequired", None)
        trade_open = cls(
            trade_id=trade_id,
            units=units,
            price=price,
            guaranteed_execution_fee=guaranteed_execution_fee,
            client_extensions=client_extensions,
            half_spread_cost=half_spread_cost,
            initial_margin_required=initial_margin_required,
        )
        trade_open.additional_properties = d
        return trade_open

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
