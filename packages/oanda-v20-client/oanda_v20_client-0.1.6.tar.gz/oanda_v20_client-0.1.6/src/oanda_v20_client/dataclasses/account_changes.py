from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .order import Order
from .position import Position
from .trade_summary import TradeSummary
from .transaction import Transaction
from typing import List, Optional, TypeVar

T = TypeVar("T", bound="AccountChanges")


@dataclasses.dataclass
class AccountChanges:
    """An AccountChanges Object is used to represent the changes to an Account's Orders, Trades and Positions since a
    specified Account TransactionID in the past.

        Attributes:
            orders_created (Union[Unset, List['Order']]): The Orders created. These Orders may have been filled, cancelled
                or triggered in the same period.
            orders_cancelled (Union[Unset, List['Order']]): The Orders cancelled.
            orders_filled (Union[Unset, List['Order']]): The Orders filled.
            orders_triggered (Union[Unset, List['Order']]): The Orders triggered.
            trades_opened (Union[Unset, List['TradeSummary']]): The Trades opened.
            trades_reduced (Union[Unset, List['TradeSummary']]): The Trades reduced.
            trades_closed (Union[Unset, List['TradeSummary']]): The Trades closed.
            positions (Union[Unset, List['Position']]): The Positions changed.
            transactions (Union[Unset, List['Transaction']]): The Transactions that have been generated."""

    orders_created: Optional[List["Order"]]
    orders_cancelled: Optional[List["Order"]]
    orders_filled: Optional[List["Order"]]
    orders_triggered: Optional[List["Order"]]
    trades_opened: Optional[List["TradeSummary"]]
    trades_reduced: Optional[List["TradeSummary"]]
    trades_closed: Optional[List["TradeSummary"]]
    positions: Optional[List["Position"]]
    transactions: Optional[List["Transaction"]]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AccountChanges":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
