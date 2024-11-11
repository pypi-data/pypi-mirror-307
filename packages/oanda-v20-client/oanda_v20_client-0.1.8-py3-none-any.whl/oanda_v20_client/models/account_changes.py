from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.transaction import Transaction
    from ..models.order import Order
    from ..models.position import Position
    from ..models.trade_summary import TradeSummary


T = TypeVar("T", bound="AccountChanges")


@_attrs_define
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
            transactions (Union[Unset, List['Transaction']]): The Transactions that have been generated.
    """

    orders_created: Union[Unset, List["Order"]] = UNSET
    orders_cancelled: Union[Unset, List["Order"]] = UNSET
    orders_filled: Union[Unset, List["Order"]] = UNSET
    orders_triggered: Union[Unset, List["Order"]] = UNSET
    trades_opened: Union[Unset, List["TradeSummary"]] = UNSET
    trades_reduced: Union[Unset, List["TradeSummary"]] = UNSET
    trades_closed: Union[Unset, List["TradeSummary"]] = UNSET
    positions: Union[Unset, List["Position"]] = UNSET
    transactions: Union[Unset, List["Transaction"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        orders_created: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.orders_created, Unset):
            orders_created = []
            for orders_created_item_data in self.orders_created:
                orders_created_item = orders_created_item_data.to_dict()
                orders_created.append(orders_created_item)

        orders_cancelled: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.orders_cancelled, Unset):
            orders_cancelled = []
            for orders_cancelled_item_data in self.orders_cancelled:
                orders_cancelled_item = orders_cancelled_item_data.to_dict()
                orders_cancelled.append(orders_cancelled_item)

        orders_filled: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.orders_filled, Unset):
            orders_filled = []
            for orders_filled_item_data in self.orders_filled:
                orders_filled_item = orders_filled_item_data.to_dict()
                orders_filled.append(orders_filled_item)

        orders_triggered: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.orders_triggered, Unset):
            orders_triggered = []
            for orders_triggered_item_data in self.orders_triggered:
                orders_triggered_item = orders_triggered_item_data.to_dict()
                orders_triggered.append(orders_triggered_item)

        trades_opened: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.trades_opened, Unset):
            trades_opened = []
            for trades_opened_item_data in self.trades_opened:
                trades_opened_item = trades_opened_item_data.to_dict()
                trades_opened.append(trades_opened_item)

        trades_reduced: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.trades_reduced, Unset):
            trades_reduced = []
            for trades_reduced_item_data in self.trades_reduced:
                trades_reduced_item = trades_reduced_item_data.to_dict()
                trades_reduced.append(trades_reduced_item)

        trades_closed: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.trades_closed, Unset):
            trades_closed = []
            for trades_closed_item_data in self.trades_closed:
                trades_closed_item = trades_closed_item_data.to_dict()
                trades_closed.append(trades_closed_item)

        positions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.positions, Unset):
            positions = []
            for positions_item_data in self.positions:
                positions_item = positions_item_data.to_dict()
                positions.append(positions_item)

        transactions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.transactions, Unset):
            transactions = []
            for transactions_item_data in self.transactions:
                transactions_item = transactions_item_data.to_dict()
                transactions.append(transactions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if orders_created is not UNSET:
            field_dict["ordersCreated"] = orders_created
        if orders_cancelled is not UNSET:
            field_dict["ordersCancelled"] = orders_cancelled
        if orders_filled is not UNSET:
            field_dict["ordersFilled"] = orders_filled
        if orders_triggered is not UNSET:
            field_dict["ordersTriggered"] = orders_triggered
        if trades_opened is not UNSET:
            field_dict["tradesOpened"] = trades_opened
        if trades_reduced is not UNSET:
            field_dict["tradesReduced"] = trades_reduced
        if trades_closed is not UNSET:
            field_dict["tradesClosed"] = trades_closed
        if positions is not UNSET:
            field_dict["positions"] = positions
        if transactions is not UNSET:
            field_dict["transactions"] = transactions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.transaction import Transaction
        from ..models.order import Order
        from ..models.position import Position
        from ..models.trade_summary import TradeSummary

        d = src_dict.copy()
        orders_created = []
        _orders_created = d.pop("ordersCreated", UNSET)
        for orders_created_item_data in _orders_created or []:
            orders_created_item = Order.from_dict(orders_created_item_data)

            orders_created.append(orders_created_item)

        orders_cancelled = []
        _orders_cancelled = d.pop("ordersCancelled", UNSET)
        for orders_cancelled_item_data in _orders_cancelled or []:
            orders_cancelled_item = Order.from_dict(orders_cancelled_item_data)

            orders_cancelled.append(orders_cancelled_item)

        orders_filled = []
        _orders_filled = d.pop("ordersFilled", UNSET)
        for orders_filled_item_data in _orders_filled or []:
            orders_filled_item = Order.from_dict(orders_filled_item_data)

            orders_filled.append(orders_filled_item)

        orders_triggered = []
        _orders_triggered = d.pop("ordersTriggered", UNSET)
        for orders_triggered_item_data in _orders_triggered or []:
            orders_triggered_item = Order.from_dict(orders_triggered_item_data)

            orders_triggered.append(orders_triggered_item)

        trades_opened = []
        _trades_opened = d.pop("tradesOpened", UNSET)
        for trades_opened_item_data in _trades_opened or []:
            trades_opened_item = TradeSummary.from_dict(trades_opened_item_data)

            trades_opened.append(trades_opened_item)

        trades_reduced = []
        _trades_reduced = d.pop("tradesReduced", UNSET)
        for trades_reduced_item_data in _trades_reduced or []:
            trades_reduced_item = TradeSummary.from_dict(trades_reduced_item_data)

            trades_reduced.append(trades_reduced_item)

        trades_closed = []
        _trades_closed = d.pop("tradesClosed", UNSET)
        for trades_closed_item_data in _trades_closed or []:
            trades_closed_item = TradeSummary.from_dict(trades_closed_item_data)

            trades_closed.append(trades_closed_item)

        positions = []
        _positions = d.pop("positions", UNSET)
        for positions_item_data in _positions or []:
            positions_item = Position.from_dict(positions_item_data)

            positions.append(positions_item)

        transactions = []
        _transactions = d.pop("transactions", UNSET)
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

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
