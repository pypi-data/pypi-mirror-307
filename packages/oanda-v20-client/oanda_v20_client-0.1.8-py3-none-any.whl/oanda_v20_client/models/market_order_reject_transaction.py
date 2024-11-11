from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.market_order_reject_transaction_position_fill import (
    check_market_order_reject_transaction_position_fill,
)
from ..models.market_order_reject_transaction_position_fill import (
    MarketOrderRejectTransactionPositionFill,
)
from ..models.market_order_reject_transaction_reason import (
    check_market_order_reject_transaction_reason,
)
from ..models.market_order_reject_transaction_reason import (
    MarketOrderRejectTransactionReason,
)
from ..models.market_order_reject_transaction_reject_reason import (
    check_market_order_reject_transaction_reject_reason,
)
from ..models.market_order_reject_transaction_reject_reason import (
    MarketOrderRejectTransactionRejectReason,
)
from ..models.market_order_reject_transaction_time_in_force import (
    check_market_order_reject_transaction_time_in_force,
)
from ..models.market_order_reject_transaction_time_in_force import (
    MarketOrderRejectTransactionTimeInForce,
)
from ..models.market_order_reject_transaction_type import (
    check_market_order_reject_transaction_type,
)
from ..models.market_order_reject_transaction_type import (
    MarketOrderRejectTransactionType,
)
from typing import Union

if TYPE_CHECKING:
    from ..models.market_order_margin_closeout import MarketOrderMarginCloseout
    from ..models.market_order_trade_close import MarketOrderTradeClose
    from ..models.stop_loss_details import StopLossDetails
    from ..models.take_profit_details import TakeProfitDetails
    from ..models.client_extensions import ClientExtensions
    from ..models.trailing_stop_loss_details import TrailingStopLossDetails
    from ..models.market_order_delayed_trade_close import MarketOrderDelayedTradeClose
    from ..models.market_order_position_closeout import MarketOrderPositionCloseout


T = TypeVar("T", bound="MarketOrderRejectTransaction")


@_attrs_define
class MarketOrderRejectTransaction:
    """A MarketOrderRejectTransaction represents the rejection of the creation of a Market Order.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, MarketOrderRejectTransactionType]): The Type of the Transaction. Always set to
            "MARKET_ORDER_REJECT" in a MarketOrderRejectTransaction.
        instrument (Union[Unset, str]): The Market Order's Instrument.
        units (Union[Unset, str]): The quantity requested to be filled by the Market Order. A posititive number of units
            results in a long Order, and a negative number of units results in a short Order.
        time_in_force (Union[Unset, MarketOrderRejectTransactionTimeInForce]): The time-in-force requested for the
            Market Order. Restricted to FOK or IOC for a MarketOrder.
        price_bound (Union[Unset, str]): The worst price that the client is willing to have the Market Order filled at.
        position_fill (Union[Unset, MarketOrderRejectTransactionPositionFill]): Specification of how Positions in the
            Account are modified when the Order is filled.
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
        reason (Union[Unset, MarketOrderRejectTransactionReason]): The reason that the Market Order was created
        client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
            clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
            your account is associated with MT4.
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
        reject_reason (Union[Unset, MarketOrderRejectTransactionRejectReason]): The reason that the Reject Transaction
            was created
    """

    id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    account_id: Union[Unset, str] = UNSET
    batch_id: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    type: Union[Unset, MarketOrderRejectTransactionType] = UNSET
    instrument: Union[Unset, str] = UNSET
    units: Union[Unset, str] = UNSET
    time_in_force: Union[Unset, MarketOrderRejectTransactionTimeInForce] = UNSET
    price_bound: Union[Unset, str] = UNSET
    position_fill: Union[Unset, MarketOrderRejectTransactionPositionFill] = UNSET
    trade_close: Union[Unset, "MarketOrderTradeClose"] = UNSET
    long_position_closeout: Union[Unset, "MarketOrderPositionCloseout"] = UNSET
    short_position_closeout: Union[Unset, "MarketOrderPositionCloseout"] = UNSET
    margin_closeout: Union[Unset, "MarketOrderMarginCloseout"] = UNSET
    delayed_trade_close: Union[Unset, "MarketOrderDelayedTradeClose"] = UNSET
    reason: Union[Unset, MarketOrderRejectTransactionReason] = UNSET
    client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    take_profit_on_fill: Union[Unset, "TakeProfitDetails"] = UNSET
    stop_loss_on_fill: Union[Unset, "StopLossDetails"] = UNSET
    trailing_stop_loss_on_fill: Union[Unset, "TrailingStopLossDetails"] = UNSET
    trade_client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    reject_reason: Union[Unset, MarketOrderRejectTransactionRejectReason] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        time = self.time

        user_id = self.user_id

        account_id = self.account_id

        batch_id = self.batch_id

        request_id = self.request_id

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

        reason: Union[Unset, str] = UNSET
        if not isinstance(self.reason, Unset):
            reason = self.reason

        client_extensions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.client_extensions, Unset):
            client_extensions = self.client_extensions.to_dict()

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

        reject_reason: Union[Unset, str] = UNSET
        if not isinstance(self.reject_reason, Unset):
            reject_reason = self.reject_reason

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if time is not UNSET:
            field_dict["time"] = time
        if user_id is not UNSET:
            field_dict["userID"] = user_id
        if account_id is not UNSET:
            field_dict["accountID"] = account_id
        if batch_id is not UNSET:
            field_dict["batchID"] = batch_id
        if request_id is not UNSET:
            field_dict["requestID"] = request_id
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
        if reason is not UNSET:
            field_dict["reason"] = reason
        if client_extensions is not UNSET:
            field_dict["clientExtensions"] = client_extensions
        if take_profit_on_fill is not UNSET:
            field_dict["takeProfitOnFill"] = take_profit_on_fill
        if stop_loss_on_fill is not UNSET:
            field_dict["stopLossOnFill"] = stop_loss_on_fill
        if trailing_stop_loss_on_fill is not UNSET:
            field_dict["trailingStopLossOnFill"] = trailing_stop_loss_on_fill
        if trade_client_extensions is not UNSET:
            field_dict["tradeClientExtensions"] = trade_client_extensions
        if reject_reason is not UNSET:
            field_dict["rejectReason"] = reject_reason

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.market_order_margin_closeout import MarketOrderMarginCloseout
        from ..models.market_order_trade_close import MarketOrderTradeClose
        from ..models.stop_loss_details import StopLossDetails
        from ..models.take_profit_details import TakeProfitDetails
        from ..models.client_extensions import ClientExtensions
        from ..models.trailing_stop_loss_details import TrailingStopLossDetails
        from ..models.market_order_delayed_trade_close import (
            MarketOrderDelayedTradeClose,
        )
        from ..models.market_order_position_closeout import MarketOrderPositionCloseout

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        time = d.pop("time", UNSET)

        user_id = d.pop("userID", UNSET)

        account_id = d.pop("accountID", UNSET)

        batch_id = d.pop("batchID", UNSET)

        request_id = d.pop("requestID", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, MarketOrderRejectTransactionType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = check_market_order_reject_transaction_type(_type)

        instrument = d.pop("instrument", UNSET)

        units = d.pop("units", UNSET)

        _time_in_force = d.pop("timeInForce", UNSET)
        time_in_force: Union[Unset, MarketOrderRejectTransactionTimeInForce]
        if isinstance(_time_in_force, Unset):
            time_in_force = UNSET
        else:
            time_in_force = check_market_order_reject_transaction_time_in_force(
                _time_in_force
            )

        price_bound = d.pop("priceBound", UNSET)

        _position_fill = d.pop("positionFill", UNSET)
        position_fill: Union[Unset, MarketOrderRejectTransactionPositionFill]
        if isinstance(_position_fill, Unset):
            position_fill = UNSET
        else:
            position_fill = check_market_order_reject_transaction_position_fill(
                _position_fill
            )

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

        _reason = d.pop("reason", UNSET)
        reason: Union[Unset, MarketOrderRejectTransactionReason]
        if isinstance(_reason, Unset):
            reason = UNSET
        else:
            reason = check_market_order_reject_transaction_reason(_reason)

        _client_extensions = d.pop("clientExtensions", UNSET)
        client_extensions: Union[Unset, ClientExtensions]
        if isinstance(_client_extensions, Unset):
            client_extensions = UNSET
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)

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

        _reject_reason = d.pop("rejectReason", UNSET)
        reject_reason: Union[Unset, MarketOrderRejectTransactionRejectReason]
        if isinstance(_reject_reason, Unset):
            reject_reason = UNSET
        else:
            reject_reason = check_market_order_reject_transaction_reject_reason(
                _reject_reason
            )

        market_order_reject_transaction = cls(
            id=id,
            time=time,
            user_id=user_id,
            account_id=account_id,
            batch_id=batch_id,
            request_id=request_id,
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
            reason=reason,
            client_extensions=client_extensions,
            take_profit_on_fill=take_profit_on_fill,
            stop_loss_on_fill=stop_loss_on_fill,
            trailing_stop_loss_on_fill=trailing_stop_loss_on_fill,
            trade_client_extensions=trade_client_extensions,
            reject_reason=reject_reason,
        )

        market_order_reject_transaction.additional_properties = d
        return market_order_reject_transaction

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
