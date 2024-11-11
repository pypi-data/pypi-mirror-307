from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.market_order_position_fill import check_market_order_position_fill
from ..models.market_order_position_fill import MarketOrderPositionFill
from ..models.market_order_state import check_market_order_state
from ..models.market_order_state import MarketOrderState
from ..models.market_order_time_in_force import check_market_order_time_in_force
from ..models.market_order_time_in_force import MarketOrderTimeInForce
from ..models.market_order_type import check_market_order_type
from ..models.market_order_type import MarketOrderType
from typing import cast
from typing import Union

if TYPE_CHECKING:
    from ..models.market_order_margin_closeout import MarketOrderMarginCloseout
    from ..models.market_order_delayed_trade_close import MarketOrderDelayedTradeClose
    from ..models.take_profit_details import TakeProfitDetails
    from ..models.stop_loss_details import StopLossDetails
    from ..models.market_order_position_closeout import MarketOrderPositionCloseout
    from ..models.trailing_stop_loss_details import TrailingStopLossDetails
    from ..models.market_order_trade_close import MarketOrderTradeClose
    from ..models.client_extensions import ClientExtensions


T = TypeVar("T", bound="MarketOrder")


@_attrs_define
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
            Order is CANCELLED)
    """

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
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        create_time = self.create_time

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state

        client_extensions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.client_extensions, Unset):
            client_extensions = self.client_extensions.to_dict()

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type

        instrument = self.instrument

        units = self.units

        time_in_force: Union[Unset, str] = UNSET
        if not isinstance(self.time_in_force, Unset):
            time_in_force = self.time_in_force

        price_bound = self.price_bound

        position_fill: Union[Unset, str] = UNSET
        if not isinstance(self.position_fill, Unset):
            position_fill = self.position_fill

        trade_close: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.trade_close, Unset):
            trade_close = self.trade_close.to_dict()

        long_position_closeout: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.long_position_closeout, Unset):
            long_position_closeout = self.long_position_closeout.to_dict()

        short_position_closeout: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.short_position_closeout, Unset):
            short_position_closeout = self.short_position_closeout.to_dict()

        margin_closeout: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.margin_closeout, Unset):
            margin_closeout = self.margin_closeout.to_dict()

        delayed_trade_close: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.delayed_trade_close, Unset):
            delayed_trade_close = self.delayed_trade_close.to_dict()

        take_profit_on_fill: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.take_profit_on_fill, Unset):
            take_profit_on_fill = self.take_profit_on_fill.to_dict()

        stop_loss_on_fill: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stop_loss_on_fill, Unset):
            stop_loss_on_fill = self.stop_loss_on_fill.to_dict()

        trailing_stop_loss_on_fill: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.trailing_stop_loss_on_fill, Unset):
            trailing_stop_loss_on_fill = self.trailing_stop_loss_on_fill.to_dict()

        trade_client_extensions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.trade_client_extensions, Unset):
            trade_client_extensions = self.trade_client_extensions.to_dict()

        filling_transaction_id = self.filling_transaction_id

        filled_time = self.filled_time

        trade_opened_id = self.trade_opened_id

        trade_reduced_id = self.trade_reduced_id

        trade_closed_i_ds: Union[Unset, List[str]] = UNSET
        if not isinstance(self.trade_closed_i_ds, Unset):
            trade_closed_i_ds = self.trade_closed_i_ds

        cancelling_transaction_id = self.cancelling_transaction_id

        cancelled_time = self.cancelled_time

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if create_time is not UNSET:
            field_dict["createTime"] = create_time
        if state is not UNSET:
            field_dict["state"] = state
        if client_extensions is not UNSET:
            field_dict["clientExtensions"] = client_extensions
        if type is not UNSET:
            field_dict["type"] = type
        if instrument is not UNSET:
            field_dict["instrument"] = instrument
        if units is not UNSET:
            field_dict["units"] = units
        if time_in_force is not UNSET:
            field_dict["timeInForce"] = time_in_force
        if price_bound is not UNSET:
            field_dict["priceBound"] = price_bound
        if position_fill is not UNSET:
            field_dict["positionFill"] = position_fill
        if trade_close is not UNSET:
            field_dict["tradeClose"] = trade_close
        if long_position_closeout is not UNSET:
            field_dict["longPositionCloseout"] = long_position_closeout
        if short_position_closeout is not UNSET:
            field_dict["shortPositionCloseout"] = short_position_closeout
        if margin_closeout is not UNSET:
            field_dict["marginCloseout"] = margin_closeout
        if delayed_trade_close is not UNSET:
            field_dict["delayedTradeClose"] = delayed_trade_close
        if take_profit_on_fill is not UNSET:
            field_dict["takeProfitOnFill"] = take_profit_on_fill
        if stop_loss_on_fill is not UNSET:
            field_dict["stopLossOnFill"] = stop_loss_on_fill
        if trailing_stop_loss_on_fill is not UNSET:
            field_dict["trailingStopLossOnFill"] = trailing_stop_loss_on_fill
        if trade_client_extensions is not UNSET:
            field_dict["tradeClientExtensions"] = trade_client_extensions
        if filling_transaction_id is not UNSET:
            field_dict["fillingTransactionID"] = filling_transaction_id
        if filled_time is not UNSET:
            field_dict["filledTime"] = filled_time
        if trade_opened_id is not UNSET:
            field_dict["tradeOpenedID"] = trade_opened_id
        if trade_reduced_id is not UNSET:
            field_dict["tradeReducedID"] = trade_reduced_id
        if trade_closed_i_ds is not UNSET:
            field_dict["tradeClosedIDs"] = trade_closed_i_ds
        if cancelling_transaction_id is not UNSET:
            field_dict["cancellingTransactionID"] = cancelling_transaction_id
        if cancelled_time is not UNSET:
            field_dict["cancelledTime"] = cancelled_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.market_order_margin_closeout import MarketOrderMarginCloseout
        from ..models.market_order_delayed_trade_close import (
            MarketOrderDelayedTradeClose,
        )
        from ..models.take_profit_details import TakeProfitDetails
        from ..models.stop_loss_details import StopLossDetails
        from ..models.market_order_position_closeout import MarketOrderPositionCloseout
        from ..models.trailing_stop_loss_details import TrailingStopLossDetails
        from ..models.market_order_trade_close import MarketOrderTradeClose
        from ..models.client_extensions import ClientExtensions

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        create_time = d.pop("createTime", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, MarketOrderState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = check_market_order_state(_state)

        _client_extensions = d.pop("clientExtensions", UNSET)
        client_extensions: Union[Unset, ClientExtensions]
        if isinstance(_client_extensions, Unset):
            client_extensions = UNSET
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)

        _type = d.pop("type", UNSET)
        type: Union[Unset, MarketOrderType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = check_market_order_type(_type)

        instrument = d.pop("instrument", UNSET)

        units = d.pop("units", UNSET)

        _time_in_force = d.pop("timeInForce", UNSET)
        time_in_force: Union[Unset, MarketOrderTimeInForce]
        if isinstance(_time_in_force, Unset):
            time_in_force = UNSET
        else:
            time_in_force = check_market_order_time_in_force(_time_in_force)

        price_bound = d.pop("priceBound", UNSET)

        _position_fill = d.pop("positionFill", UNSET)
        position_fill: Union[Unset, MarketOrderPositionFill]
        if isinstance(_position_fill, Unset):
            position_fill = UNSET
        else:
            position_fill = check_market_order_position_fill(_position_fill)

        _trade_close = d.pop("tradeClose", UNSET)
        trade_close: Union[Unset, MarketOrderTradeClose]
        if isinstance(_trade_close, Unset):
            trade_close = UNSET
        else:
            trade_close = MarketOrderTradeClose.from_dict(_trade_close)

        _long_position_closeout = d.pop("longPositionCloseout", UNSET)
        long_position_closeout: Union[Unset, MarketOrderPositionCloseout]
        if isinstance(_long_position_closeout, Unset):
            long_position_closeout = UNSET
        else:
            long_position_closeout = MarketOrderPositionCloseout.from_dict(
                _long_position_closeout
            )

        _short_position_closeout = d.pop("shortPositionCloseout", UNSET)
        short_position_closeout: Union[Unset, MarketOrderPositionCloseout]
        if isinstance(_short_position_closeout, Unset):
            short_position_closeout = UNSET
        else:
            short_position_closeout = MarketOrderPositionCloseout.from_dict(
                _short_position_closeout
            )

        _margin_closeout = d.pop("marginCloseout", UNSET)
        margin_closeout: Union[Unset, MarketOrderMarginCloseout]
        if isinstance(_margin_closeout, Unset):
            margin_closeout = UNSET
        else:
            margin_closeout = MarketOrderMarginCloseout.from_dict(_margin_closeout)

        _delayed_trade_close = d.pop("delayedTradeClose", UNSET)
        delayed_trade_close: Union[Unset, MarketOrderDelayedTradeClose]
        if isinstance(_delayed_trade_close, Unset):
            delayed_trade_close = UNSET
        else:
            delayed_trade_close = MarketOrderDelayedTradeClose.from_dict(
                _delayed_trade_close
            )

        _take_profit_on_fill = d.pop("takeProfitOnFill", UNSET)
        take_profit_on_fill: Union[Unset, TakeProfitDetails]
        if isinstance(_take_profit_on_fill, Unset):
            take_profit_on_fill = UNSET
        else:
            take_profit_on_fill = TakeProfitDetails.from_dict(_take_profit_on_fill)

        _stop_loss_on_fill = d.pop("stopLossOnFill", UNSET)
        stop_loss_on_fill: Union[Unset, StopLossDetails]
        if isinstance(_stop_loss_on_fill, Unset):
            stop_loss_on_fill = UNSET
        else:
            stop_loss_on_fill = StopLossDetails.from_dict(_stop_loss_on_fill)

        _trailing_stop_loss_on_fill = d.pop("trailingStopLossOnFill", UNSET)
        trailing_stop_loss_on_fill: Union[Unset, TrailingStopLossDetails]
        if isinstance(_trailing_stop_loss_on_fill, Unset):
            trailing_stop_loss_on_fill = UNSET
        else:
            trailing_stop_loss_on_fill = TrailingStopLossDetails.from_dict(
                _trailing_stop_loss_on_fill
            )

        _trade_client_extensions = d.pop("tradeClientExtensions", UNSET)
        trade_client_extensions: Union[Unset, ClientExtensions]
        if isinstance(_trade_client_extensions, Unset):
            trade_client_extensions = UNSET
        else:
            trade_client_extensions = ClientExtensions.from_dict(
                _trade_client_extensions
            )

        filling_transaction_id = d.pop("fillingTransactionID", UNSET)

        filled_time = d.pop("filledTime", UNSET)

        trade_opened_id = d.pop("tradeOpenedID", UNSET)

        trade_reduced_id = d.pop("tradeReducedID", UNSET)

        trade_closed_i_ds = cast(List[str], d.pop("tradeClosedIDs", UNSET))

        cancelling_transaction_id = d.pop("cancellingTransactionID", UNSET)

        cancelled_time = d.pop("cancelledTime", UNSET)

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
