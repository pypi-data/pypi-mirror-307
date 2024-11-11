from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .client_extensions import ClientExtensions
from .market_order_delayed_trade_close import MarketOrderDelayedTradeClose
from .market_order_margin_closeout import MarketOrderMarginCloseout
from .market_order_position_closeout import MarketOrderPositionCloseout
from .market_order_position_fill import MarketOrderPositionFill
from .market_order_state import MarketOrderState
from .market_order_time_in_force import MarketOrderTimeInForce
from .market_order_trade_close import MarketOrderTradeClose
from .market_order_type import MarketOrderType
from .stop_loss_details import StopLossDetails
from .take_profit_details import TakeProfitDetails
from .trailing_stop_loss_details import TrailingStopLossDetails
from typing import List, TypeVar, Union

T = TypeVar("T", bound="MarketOrder")


@dataclasses.dataclass
class MarketOrder:
    """A MarketOrder is an order that is filled immediately upon creation using the current market price.

    Attributes:
        id (Union[Unset, str]): The Order's identifier, unique within the Order's Account.
        create_time (Union[Unset, str]): The time when the Order was created.
        state (Union[Unset, MarketOrderState]): The current state of the Order.
        client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
            clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
            your account is associated with MT4.
        type (Union[Unset, MarketOrderType]): The type of the Order. Always set to "MARKET" for Market Orders.
        instrument (Union[Unset, str]): The Market Order's Instrument.
        units (Union[Unset, str]): The quantity requested to be filled by the Market Order. A posititive number of units
            results in a long Order, and a negative number of units results in a short Order.
        time_in_force (Union[Unset, MarketOrderTimeInForce]): The time-in-force requested for the Market Order.
            Restricted to FOK or IOC for a MarketOrder.
        price_bound (Union[Unset, str]): The worst price that the client is willing to have the Market Order filled at.
        position_fill (Union[Unset, MarketOrderPositionFill]): Specification of how Positions in the Account are
            modified when the Order is filled.
        trade_close (Union[Unset, MarketOrderTradeClose]): A MarketOrderTradeClose specifies the extensions to a Market
            Order that has been created specifically to close a Trade.
        long_position_closeout (Union[Unset, MarketOrderPositionCloseout]): A MarketOrderPositionCloseout specifies the
            extensions to a Market Order when it has been created to closeout a specific Position.
        short_position_closeout (Union[Unset, MarketOrderPositionCloseout]): A MarketOrderPositionCloseout specifies the
            extensions to a Market Order when it has been created to closeout a specific Position.
        margin_closeout (Union[Unset, MarketOrderMarginCloseout]): Details for the Market Order extensions specific to a
            Market Order placed that is part of a Market Order Margin Closeout in a client's account
        delayed_trade_close (Union[Unset, MarketOrderDelayedTradeClose]): Details for the Market Order extensions
            specific to a Market Order placed with the intent of fully closing a specific open trade that should have
            already been closed but wasn't due to halted market conditions
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

    id: Union[Unset, str] = UNSET
    create_time: Union[Unset, str] = UNSET
    state: Union[Unset, MarketOrderState] = UNSET
    client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    type: Union[Unset, MarketOrderType] = UNSET
    instrument: Union[Unset, str] = UNSET
    units: Union[Unset, str] = UNSET
    time_in_force: Union[Unset, MarketOrderTimeInForce] = UNSET
    price_bound: Union[Unset, str] = UNSET
    position_fill: Union[Unset, MarketOrderPositionFill] = UNSET
    trade_close: Union[Unset, "MarketOrderTradeClose"] = UNSET
    long_position_closeout: Union[Unset, "MarketOrderPositionCloseout"] = UNSET
    short_position_closeout: Union[Unset, "MarketOrderPositionCloseout"] = UNSET
    margin_closeout: Union[Unset, "MarketOrderMarginCloseout"] = UNSET
    delayed_trade_close: Union[Unset, "MarketOrderDelayedTradeClose"] = UNSET
    take_profit_on_fill: Union[Unset, "TakeProfitDetails"] = UNSET
    stop_loss_on_fill: Union[Unset, "StopLossDetails"] = UNSET
    trailing_stop_loss_on_fill: Union[Unset, "TrailingStopLossDetails"] = UNSET
    trade_client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    filling_transaction_id: Union[Unset, str] = UNSET
    filled_time: Union[Unset, str] = UNSET
    trade_opened_id: Union[Unset, str] = UNSET
    trade_reduced_id: Union[Unset, str] = UNSET
    trade_closed_i_ds: Union[Unset, List[str]] = UNSET
    cancelling_transaction_id: Union[Unset, str] = UNSET
    cancelled_time: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MarketOrder":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
