from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_extensions import ClientExtensions
from .market_order_delayed_trade_close import MarketOrderDelayedTradeClose
from .market_order_margin_closeout import MarketOrderMarginCloseout
from .market_order_position_closeout import MarketOrderPositionCloseout
from .market_order_position_fill import MarketOrderPositionFill
from .market_order_position_fill import check_market_order_position_fill
from .market_order_state import MarketOrderState
from .market_order_state import check_market_order_state
from .market_order_time_in_force import MarketOrderTimeInForce
from .market_order_time_in_force import check_market_order_time_in_force
from .market_order_trade_close import MarketOrderTradeClose
from .market_order_type import MarketOrderType
from .market_order_type import check_market_order_type
from .stop_loss_details import StopLossDetails
from .take_profit_details import TakeProfitDetails
from .trailing_stop_loss_details import TrailingStopLossDetails
from types import Unset
from typing import List, Optional, Type, TypeVar, cast

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

    id: Optional[str]
    create_time: Optional[str]
    state: Optional[MarketOrderState]
    client_extensions: Optional["ClientExtensions"]
    type: Optional[MarketOrderType]
    instrument: Optional[str]
    units: Optional[str]
    time_in_force: Optional[MarketOrderTimeInForce]
    price_bound: Optional[str]
    position_fill: Optional[MarketOrderPositionFill]
    trade_close: Optional["MarketOrderTradeClose"]
    long_position_closeout: Optional["MarketOrderPositionCloseout"]
    short_position_closeout: Optional["MarketOrderPositionCloseout"]
    margin_closeout: Optional["MarketOrderMarginCloseout"]
    delayed_trade_close: Optional["MarketOrderDelayedTradeClose"]
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

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .market_order_margin_closeout import MarketOrderMarginCloseout
        from .market_order_trade_close import MarketOrderTradeClose
        from .stop_loss_details import StopLossDetails
        from .take_profit_details import TakeProfitDetails
        from .client_extensions import ClientExtensions
        from .trailing_stop_loss_details import TrailingStopLossDetails
        from .market_order_delayed_trade_close import MarketOrderDelayedTradeClose
        from .market_order_position_closeout import MarketOrderPositionCloseout

        d = src_dict.copy()
        id = d.pop("id", None)
        create_time = d.pop("createTime", None)
        _state = d.pop("state", None)
        state: Optional[MarketOrderState]
        if isinstance(_state, Unset):
            state = None
        else:
            state = check_market_order_state(_state)
        _client_extensions = d.pop("clientExtensions", None)
        client_extensions: Optional[ClientExtensions]
        if isinstance(_client_extensions, Unset):
            client_extensions = None
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)
        _type = d.pop("type", None)
        type: Optional[MarketOrderType]
        if _type is None:
            type = None
        else:
            type = check_market_order_type(_type)
        instrument = d.pop("instrument", None)
        units = d.pop("units", None)
        _time_in_force = d.pop("timeInForce", None)
        time_in_force: Optional[MarketOrderTimeInForce]
        if isinstance(_time_in_force, Unset):
            time_in_force = None
        else:
            time_in_force = check_market_order_time_in_force(_time_in_force)
        price_bound = d.pop("priceBound", None)
        _position_fill = d.pop("positionFill", None)
        position_fill: Optional[MarketOrderPositionFill]
        if isinstance(_position_fill, Unset):
            position_fill = None
        else:
            position_fill = check_market_order_position_fill(_position_fill)
        _trade_close = d.pop("tradeClose", None)
        trade_close: Optional[MarketOrderTradeClose]
        if isinstance(_trade_close, Unset):
            trade_close = None
        else:
            trade_close = MarketOrderTradeClose.from_dict(_trade_close)
        _long_position_closeout = d.pop("longPositionCloseout", None)
        long_position_closeout: Optional[MarketOrderPositionCloseout]
        if isinstance(_long_position_closeout, Unset):
            long_position_closeout = None
        else:
            long_position_closeout = MarketOrderPositionCloseout.from_dict(
                _long_position_closeout
            )
        _short_position_closeout = d.pop("shortPositionCloseout", None)
        short_position_closeout: Optional[MarketOrderPositionCloseout]
        if isinstance(_short_position_closeout, Unset):
            short_position_closeout = None
        else:
            short_position_closeout = MarketOrderPositionCloseout.from_dict(
                _short_position_closeout
            )
        _margin_closeout = d.pop("marginCloseout", None)
        margin_closeout: Optional[MarketOrderMarginCloseout]
        if isinstance(_margin_closeout, Unset):
            margin_closeout = None
        else:
            margin_closeout = MarketOrderMarginCloseout.from_dict(_margin_closeout)
        _delayed_trade_close = d.pop("delayedTradeClose", None)
        delayed_trade_close: Optional[MarketOrderDelayedTradeClose]
        if isinstance(_delayed_trade_close, Unset):
            delayed_trade_close = None
        else:
            delayed_trade_close = MarketOrderDelayedTradeClose.from_dict(
                _delayed_trade_close
            )
        _take_profit_on_fill = d.pop("takeProfitOnFill", None)
        take_profit_on_fill: Optional[TakeProfitDetails]
        if isinstance(_take_profit_on_fill, Unset):
            take_profit_on_fill = None
        else:
            take_profit_on_fill = TakeProfitDetails.from_dict(_take_profit_on_fill)
        _stop_loss_on_fill = d.pop("stopLossOnFill", None)
        stop_loss_on_fill: Optional[StopLossDetails]
        if isinstance(_stop_loss_on_fill, Unset):
            stop_loss_on_fill = None
        else:
            stop_loss_on_fill = StopLossDetails.from_dict(_stop_loss_on_fill)
        _trailing_stop_loss_on_fill = d.pop("trailingStopLossOnFill", None)
        trailing_stop_loss_on_fill: Optional[TrailingStopLossDetails]
        if isinstance(_trailing_stop_loss_on_fill, Unset):
            trailing_stop_loss_on_fill = None
        else:
            trailing_stop_loss_on_fill = TrailingStopLossDetails.from_dict(
                _trailing_stop_loss_on_fill
            )
        _trade_client_extensions = d.pop("tradeClientExtensions", None)
        trade_client_extensions: Optional[ClientExtensions]
        if isinstance(_trade_client_extensions, Unset):
            trade_client_extensions = None
        else:
            trade_client_extensions = ClientExtensions.from_dict(
                _trade_client_extensions
            )
        filling_transaction_id = d.pop("fillingTransactionID", None)
        filled_time = d.pop("filledTime", None)
        trade_opened_id = d.pop("tradeOpenedID", None)
        trade_reduced_id = d.pop("tradeReducedID", None)
        trade_closed_i_ds = cast(List[str], d.pop("tradeClosedIDs", None))
        cancelling_transaction_id = d.pop("cancellingTransactionID", None)
        cancelled_time = d.pop("cancelledTime", None)
        market_order = cls(
            id=id,
            create_time=create_time,
            state=state,
            client_extensions=client_extensions,
            type=type,
            instrument=instrument,
            units=units,
            time_in_force=time_in_force,
            price_bound=price_bound,
            position_fill=position_fill,
            trade_close=trade_close,
            long_position_closeout=long_position_closeout,
            short_position_closeout=short_position_closeout,
            margin_closeout=margin_closeout,
            delayed_trade_close=delayed_trade_close,
            take_profit_on_fill=take_profit_on_fill,
            stop_loss_on_fill=stop_loss_on_fill,
            trailing_stop_loss_on_fill=trailing_stop_loss_on_fill,
            trade_client_extensions=trade_client_extensions,
            filling_transaction_id=filling_transaction_id,
            filled_time=filled_time,
            trade_opened_id=trade_opened_id,
            trade_reduced_id=trade_reduced_id,
            trade_closed_i_ds=trade_closed_i_ds,
            cancelling_transaction_id=cancelling_transaction_id,
            cancelled_time=cancelled_time,
        )
        market_order.additional_properties = d
        return market_order

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
