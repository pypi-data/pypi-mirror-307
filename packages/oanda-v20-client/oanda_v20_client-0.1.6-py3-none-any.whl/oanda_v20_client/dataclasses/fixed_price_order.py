from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .client_extensions import ClientExtensions
from .fixed_price_order_position_fill import FixedPriceOrderPositionFill
from .fixed_price_order_state import FixedPriceOrderState
from .fixed_price_order_type import FixedPriceOrderType
from .stop_loss_details import StopLossDetails
from .take_profit_details import TakeProfitDetails
from .trailing_stop_loss_details import TrailingStopLossDetails
from typing import List, Optional, TypeVar

T = TypeVar("T", bound="FixedPriceOrder")


@dataclasses.dataclass
class FixedPriceOrder:
    """A FixedPriceOrder is an order that is filled immediately upon creation using a fixed price.

    Attributes:
        id (Union[Unset, str]): The Order's identifier, unique within the Order's Account.
        create_time (Union[Unset, str]): The time when the Order was created.
        state (Union[Unset, FixedPriceOrderState]): The current state of the Order.
        client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
            clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
            your account is associated with MT4.
        type (Union[Unset, FixedPriceOrderType]): The type of the Order. Always set to "FIXED_PRICE" for Fixed Price
            Orders.
        instrument (Union[Unset, str]): The Fixed Price Order's Instrument.
        units (Union[Unset, str]): The quantity requested to be filled by the Fixed Price Order. A posititive number of
            units results in a long Order, and a negative number of units results in a short Order.
        price (Union[Unset, str]): The price specified for the Fixed Price Order. This price is the exact price that the
            Fixed Price Order will be filled at.
        position_fill (Union[Unset, FixedPriceOrderPositionFill]): Specification of how Positions in the Account are
            modified when the Order is filled.
        trade_state (Union[Unset, str]): The state that the trade resulting from the Fixed Price Order should be set to.
        take_profit_on_fill (Union[Unset, TakeProfitDetails]): TakeProfitDetails specifies the details of a Take Profit
            Order to be created on behalf of a client. This may happen when an Order is filled that opens a Trade requiring
            a Take Profit, or when a Trade's dependent Take Profit Order is modified directly through the Trade.
        stop_loss_on_fill (Union[Unset, StopLossDetails]): StopLossDetails specifies the details of a Stop Loss Order to
            be created on behalf of a client. This may happen when an Order is filled that opens a Trade requiring a Stop
            Loss, or when a Trade's dependent Stop Loss Order is modified directly through the Trade.
        trailing_stop_loss_on_fill (Union[Unset, TrailingStopLossDetails]): TrailingStopLossDetails specifies the
            details of a Trailing Stop Loss Order to be created on behalf of a client. This may happen when an Order is
            filled that opens a Trade requiring a Trailing Stop Loss, or when a Trade's dependent Trailing Stop Loss Order
            is modified directly through the Trade.
        trade_client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
            clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
            your account is associated with MT4.
        filling_transaction_id (Union[Unset, str]): ID of the Transaction that filled this Order (only provided when the
            Order's state is FILLED)
        filled_time (Union[Unset, str]): Date/time when the Order was filled (only provided when the Order's state is
            FILLED)
        trade_opened_id (Union[Unset, str]): Trade ID of Trade opened when the Order was filled (only provided when the
            Order's state is FILLED and a Trade was opened as a result of the fill)
        trade_reduced_id (Union[Unset, str]): Trade ID of Trade reduced when the Order was filled (only provided when
            the Order's state is FILLED and a Trade was reduced as a result of the fill)
        trade_closed_i_ds (Union[Unset, List[str]]): Trade IDs of Trades closed when the Order was filled (only provided
            when the Order's state is FILLED and one or more Trades were closed as a result of the fill)
        cancelling_transaction_id (Union[Unset, str]): ID of the Transaction that cancelled the Order (only provided
            when the Order's state is CANCELLED)
        cancelled_time (Union[Unset, str]): Date/time when the Order was cancelled (only provided when the state of the
            Order is CANCELLED)"""

    id: Optional[str]
    create_time: Optional[str]
    state: Optional[FixedPriceOrderState]
    client_extensions: Optional["ClientExtensions"]
    type: Optional[FixedPriceOrderType]
    instrument: Optional[str]
    units: Optional[str]
    price: Optional[str]
    position_fill: Optional[FixedPriceOrderPositionFill]
    trade_state: Optional[str]
    take_profit_on_fill: Optional["TakeProfitDetails"]
    stop_loss_on_fill: Optional["StopLossDetails"]
    trailing_stop_loss_on_fill: Optional["TrailingStopLossDetails"]
    trade_client_extensions: Optional["ClientExtensions"]
    filling_transaction_id: Optional[str]
    filled_time: Optional[str]
    trade_opened_id: Optional[str]
    trade_reduced_id: Optional[str]
    trade_closed_i_ds: Optional[List[str]]
    cancelling_transaction_id: Optional[str]
    cancelled_time: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FixedPriceOrder":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
