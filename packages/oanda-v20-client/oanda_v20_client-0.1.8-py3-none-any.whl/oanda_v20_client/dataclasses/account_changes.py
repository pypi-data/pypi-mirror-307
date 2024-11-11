from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .order import Order
from .position import Position
from .trade_summary import TradeSummary
from .transaction import Transaction
from typing import List, Optional, Type, TypeVar

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

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .transaction import Transaction
        from .order import Order
        from .position import Position
        from .trade_summary import TradeSummary

        d = src_dict.copy()
        orders_created = []
        _orders_created = d.pop("ordersCreated", None)
        for orders_created_item_data in _orders_created or []:
            orders_created_item = Order.from_dict(orders_created_item_data)
            orders_created.append(orders_created_item)
        orders_cancelled = []
        _orders_cancelled = d.pop("ordersCancelled", None)
        for orders_cancelled_item_data in _orders_cancelled or []:
            orders_cancelled_item = Order.from_dict(orders_cancelled_item_data)
            orders_cancelled.append(orders_cancelled_item)
        orders_filled = []
        _orders_filled = d.pop("ordersFilled", None)
        for orders_filled_item_data in _orders_filled or []:
            orders_filled_item = Order.from_dict(orders_filled_item_data)
            orders_filled.append(orders_filled_item)
        orders_triggered = []
        _orders_triggered = d.pop("ordersTriggered", None)
        for orders_triggered_item_data in _orders_triggered or []:
            orders_triggered_item = Order.from_dict(orders_triggered_item_data)
            orders_triggered.append(orders_triggered_item)
        trades_opened = []
        _trades_opened = d.pop("tradesOpened", None)
        for trades_opened_item_data in _trades_opened or []:
            trades_opened_item = TradeSummary.from_dict(trades_opened_item_data)
            trades_opened.append(trades_opened_item)
        trades_reduced = []
        _trades_reduced = d.pop("tradesReduced", None)
        for trades_reduced_item_data in _trades_reduced or []:
            trades_reduced_item = TradeSummary.from_dict(trades_reduced_item_data)
            trades_reduced.append(trades_reduced_item)
        trades_closed = []
        _trades_closed = d.pop("tradesClosed", None)
        for trades_closed_item_data in _trades_closed or []:
            trades_closed_item = TradeSummary.from_dict(trades_closed_item_data)
            trades_closed.append(trades_closed_item)
        positions = []
        _positions = d.pop("positions", None)
        for positions_item_data in _positions or []:
            positions_item = Position.from_dict(positions_item_data)
            positions.append(positions_item)
        transactions = []
        _transactions = d.pop("transactions", None)
        for transactions_item_data in _transactions or []:
            transactions_item = Transaction.from_dict(transactions_item_data)
            transactions.append(transactions_item)
        account_changes = cls(
            orders_created=orders_created,
            orders_cancelled=orders_cancelled,
            orders_filled=orders_filled,
            orders_triggered=orders_triggered,
            trades_opened=trades_opened,
            trades_reduced=trades_reduced,
            trades_closed=trades_closed,
            positions=positions,
            transactions=transactions,
        )
        account_changes.additional_properties = d
        return account_changes

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
