from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import List, Optional, Type, TypeVar, cast

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

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        units = d.pop("units", None)
        average_price = d.pop("averagePrice", None)
        trade_i_ds = cast(List[str], d.pop("tradeIDs", None))
        pl = d.pop("pl", None)
        unrealized_pl = d.pop("unrealizedPL", None)
        resettable_pl = d.pop("resettablePL", None)
        financing = d.pop("financing", None)
        guaranteed_execution_fees = d.pop("guaranteedExecutionFees", None)
        position_side = cls(
            units=units,
            average_price=average_price,
            trade_i_ds=trade_i_ds,
            pl=pl,
            unrealized_pl=unrealized_pl,
            resettable_pl=resettable_pl,
            financing=financing,
            guaranteed_execution_fees=guaranteed_execution_fees,
        )
        position_side.additional_properties = d
        return position_side

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
