from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.fixed_price_order_transaction_position_fill import (
    check_fixed_price_order_transaction_position_fill,
)
from ..models.fixed_price_order_transaction_position_fill import (
    FixedPriceOrderTransactionPositionFill,
)
from ..models.fixed_price_order_transaction_reason import (
    check_fixed_price_order_transaction_reason,
)
from ..models.fixed_price_order_transaction_reason import (
    FixedPriceOrderTransactionReason,
)
from ..models.fixed_price_order_transaction_type import (
    check_fixed_price_order_transaction_type,
)
from ..models.fixed_price_order_transaction_type import FixedPriceOrderTransactionType
from typing import Union

if TYPE_CHECKING:
    from ..models.client_extensions import ClientExtensions
    from ..models.stop_loss_details import StopLossDetails
    from ..models.trailing_stop_loss_details import TrailingStopLossDetails
    from ..models.take_profit_details import TakeProfitDetails


T = TypeVar("T", bound="FixedPriceOrderTransaction")


@_attrs_define
class FixedPriceOrderTransaction:
    """A FixedPriceOrderTransaction represents the creation of a Fixed Price Order in the user's account. A Fixed Price
    Order is an Order that is filled immediately at a specified price.

        Attributes:
            id (Union[Unset, str]): The Transaction's Identifier.
            time (Union[Unset, str]): The date/time when the Transaction was created.
            user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
            account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
            batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
                batch are applied to the Account simultaneously.
            request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
            type (Union[Unset, FixedPriceOrderTransactionType]): The Type of the Transaction. Always set to
                "FIXED_PRICE_ORDER" in a FixedPriceOrderTransaction.
            instrument (Union[Unset, str]): The Fixed Price Order's Instrument.
            units (Union[Unset, str]): The quantity requested to be filled by the Fixed Price Order. A posititive number of
                units results in a long Order, and a negative number of units results in a short Order.
            price (Union[Unset, str]): The price specified for the Fixed Price Order. This price is the exact price that the
                Fixed Price Order will be filled at.
            position_fill (Union[Unset, FixedPriceOrderTransactionPositionFill]): Specification of how Positions in the
                Account are modified when the Order is filled.
            trade_state (Union[Unset, str]): The state that the trade resulting from the Fixed Price Order should be set to.
            reason (Union[Unset, FixedPriceOrderTransactionReason]): The reason that the Fixed Price Order was created
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
    """

    id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    account_id: Union[Unset, str] = UNSET
    batch_id: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    type: Union[Unset, FixedPriceOrderTransactionType] = UNSET
    instrument: Union[Unset, str] = UNSET
    units: Union[Unset, str] = UNSET
    price: Union[Unset, str] = UNSET
    position_fill: Union[Unset, FixedPriceOrderTransactionPositionFill] = UNSET
    trade_state: Union[Unset, str] = UNSET
    reason: Union[Unset, FixedPriceOrderTransactionReason] = UNSET
    client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    take_profit_on_fill: Union[Unset, "TakeProfitDetails"] = UNSET
    stop_loss_on_fill: Union[Unset, "StopLossDetails"] = UNSET
    trailing_stop_loss_on_fill: Union[Unset, "TrailingStopLossDetails"] = UNSET
    trade_client_extensions: Union[Unset, "ClientExtensions"] = UNSET
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

        price = self.price

        position_fill: Union[Unset, str] = UNSET
        if not isinstance(self.position_fill, Unset):
            position_fill = self.position_fill

        trade_state = self.trade_state

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
        if price is not UNSET:
            field_dict["price"] = price
        if position_fill is not UNSET:
            field_dict["positionFill"] = position_fill
        if trade_state is not UNSET:
            field_dict["tradeState"] = trade_state
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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.client_extensions import ClientExtensions
        from ..models.stop_loss_details import StopLossDetails
        from ..models.trailing_stop_loss_details import TrailingStopLossDetails
        from ..models.take_profit_details import TakeProfitDetails

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        time = d.pop("time", UNSET)

        user_id = d.pop("userID", UNSET)

        account_id = d.pop("accountID", UNSET)

        batch_id = d.pop("batchID", UNSET)

        request_id = d.pop("requestID", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, FixedPriceOrderTransactionType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = check_fixed_price_order_transaction_type(_type)

        instrument = d.pop("instrument", UNSET)

        units = d.pop("units", UNSET)

        price = d.pop("price", UNSET)

        _position_fill = d.pop("positionFill", UNSET)
        position_fill: Union[Unset, FixedPriceOrderTransactionPositionFill]
        if isinstance(_position_fill, Unset):
            position_fill = UNSET
        else:
            position_fill = check_fixed_price_order_transaction_position_fill(
                _position_fill
            )

        trade_state = d.pop("tradeState", UNSET)

        _reason = d.pop("reason", UNSET)
        reason: Union[Unset, FixedPriceOrderTransactionReason]
        if isinstance(_reason, Unset):
            reason = UNSET
        else:
            reason = check_fixed_price_order_transaction_reason(_reason)

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

        fixed_price_order_transaction = cls(
            id=id,
            time=time,
            user_id=user_id,
            account_id=account_id,
            batch_id=batch_id,
            request_id=request_id,
            type=type,
            instrument=instrument,
            units=units,
            price=price,
            position_fill=position_fill,
            trade_state=trade_state,
            reason=reason,
            client_extensions=client_extensions,
            take_profit_on_fill=take_profit_on_fill,
            stop_loss_on_fill=stop_loss_on_fill,
            trailing_stop_loss_on_fill=trailing_stop_loss_on_fill,
            trade_client_extensions=trade_client_extensions,
        )

        fixed_price_order_transaction.additional_properties = d
        return fixed_price_order_transaction

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
