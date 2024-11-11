from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from typing import List, Optional, TypeVar

T = TypeVar("T", bound="PositionSide")


@dataclasses.dataclass
class PositionSide:
    """The representation of a Position for a single direction (long or short).

    Attributes:
        units (Union[Unset, str]): Number of units in the position (negative value indicates short position, positive
            indicates long position).
        average_price (Union[Unset, str]): Volume-weighted average of the underlying Trade open prices for the Position.
        trade_i_ds (Union[Unset, List[str]]): List of the open Trade IDs which contribute to the open Position.
        pl (Union[Unset, str]): Profit/loss realized by the PositionSide over the lifetime of the Account.
        unrealized_pl (Union[Unset, str]): The unrealized profit/loss of all open Trades that contribute to this
            PositionSide.
        resettable_pl (Union[Unset, str]): Profit/loss realized by the PositionSide since the Account's resettablePL was
            last reset by the client.
        financing (Union[Unset, str]): The total amount of financing paid/collected for this PositionSide over the
            lifetime of the Account.
        guaranteed_execution_fees (Union[Unset, str]): The total amount of fees charged over the lifetime of the Account
            for the execution of guaranteed Stop Loss Orders attached to Trades for this PositionSide."""

    units: Optional[str]
    average_price: Optional[str]
    trade_i_ds: Optional[List[str]]
    pl: Optional[str]
    unrealized_pl: Optional[str]
    resettable_pl: Optional[str]
    financing: Optional[str]
    guaranteed_execution_fees: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PositionSide":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
