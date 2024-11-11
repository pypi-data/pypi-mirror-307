from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .market_order_transaction import MarketOrderTransaction
from .order_cancel_transaction import OrderCancelTransaction
from .order_fill_transaction import OrderFillTransaction
from typing import List, TypeVar, Union

T = TypeVar("T", bound="ClosePositionResponse200")


@dataclasses.dataclass
class ClosePositionResponse200:
    """Attributes:
    long_order_create_transaction (Union[Unset, MarketOrderTransaction]): A MarketOrderTransaction represents the
        creation of a Market Order in the user's account. A Market Order is an Order that is filled immediately at the
        current market price.
        Market Orders can be specialized when they are created to accomplish a specific task: to close a Trade, to
        closeout a Position or to particiate in in a Margin closeout.
    long_order_fill_transaction (Union[Unset, OrderFillTransaction]): An OrderFillTransaction represents the filling
        of an Order in the client's Account.
    long_order_cancel_transaction (Union[Unset, OrderCancelTransaction]): An OrderCancelTransaction represents the
        cancellation of an Order in the client's Account.
    short_order_create_transaction (Union[Unset, MarketOrderTransaction]): A MarketOrderTransaction represents the
        creation of a Market Order in the user's account. A Market Order is an Order that is filled immediately at the
        current market price.
        Market Orders can be specialized when they are created to accomplish a specific task: to close a Trade, to
        closeout a Position or to particiate in in a Margin closeout.
    short_order_fill_transaction (Union[Unset, OrderFillTransaction]): An OrderFillTransaction represents the
        filling of an Order in the client's Account.
    short_order_cancel_transaction (Union[Unset, OrderCancelTransaction]): An OrderCancelTransaction represents the
        cancellation of an Order in the client's Account.
    related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
        satisfying the request.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    long_order_create_transaction: Union[Unset, "MarketOrderTransaction"] = UNSET
    long_order_fill_transaction: Union[Unset, "OrderFillTransaction"] = UNSET
    long_order_cancel_transaction: Union[Unset, "OrderCancelTransaction"] = UNSET
    short_order_create_transaction: Union[Unset, "MarketOrderTransaction"] = UNSET
    short_order_fill_transaction: Union[Unset, "OrderFillTransaction"] = UNSET
    short_order_cancel_transaction: Union[Unset, "OrderCancelTransaction"] = UNSET
    related_transaction_i_ds: Union[Unset, List[str]] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClosePositionResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
