from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_extensions import ClientExtensions
from .trailing_stop_loss_order_request_time_in_force import (
    TrailingStopLossOrderRequestTimeInForce,
)
from .trailing_stop_loss_order_request_time_in_force import (
    check_trailing_stop_loss_order_request_time_in_force,
)
from .trailing_stop_loss_order_request_trigger_condition import (
    TrailingStopLossOrderRequestTriggerCondition,
)
from .trailing_stop_loss_order_request_trigger_condition import (
    check_trailing_stop_loss_order_request_trigger_condition,
)
from .trailing_stop_loss_order_request_type import TrailingStopLossOrderRequestType
from .trailing_stop_loss_order_request_type import (
    check_trailing_stop_loss_order_request_type,
)
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="TrailingStopLossOrderRequest")


@dataclasses.dataclass
class TrailingStopLossOrderRequest:
    """A TrailingStopLossOrderRequest specifies the parameters that may be set when creating a Trailing Stop Loss Order.

    Attributes:
        type (Union[Unset, TrailingStopLossOrderRequestType]): The type of the Order to Create. Must be set to
            "TRAILING_STOP_LOSS" when creating a Trailng Stop Loss Order.
        trade_id (Union[Unset, str]): The ID of the Trade to close when the price threshold is breached.
        client_trade_id (Union[Unset, str]): The client ID of the Trade to be closed when the price threshold is
            breached.
        distance (Union[Unset, str]): The price distance (in price units) specified for the TrailingStopLoss Order.
        time_in_force (Union[Unset, TrailingStopLossOrderRequestTimeInForce]): The time-in-force requested for the
            TrailingStopLoss Order. Restricted to "GTC", "GFD" and "GTD" for TrailingStopLoss Orders.
        gtd_time (Union[Unset, str]): The date/time when the StopLoss Order will be cancelled if its timeInForce is
            "GTD".
        trigger_condition (Union[Unset, TrailingStopLossOrderRequestTriggerCondition]): Specification of which price
            component should be used when determining if an Order should be triggered and filled. This allows Orders to be
            triggered based on the bid, ask, mid, default (ask for buy, bid for sell) or inverse (ask for sell, bid for buy)
            price depending on the desired behaviour. Orders are always filled using their default price component.
            This feature is only provided through the REST API. Clients who choose to specify a non-default trigger
            condition will not see it reflected in any of OANDA's proprietary or partner trading platforms, their
            transaction history or their account statements. OANDA platforms always assume that an Order's trigger condition
            is set to the default value when indicating the distance from an Order's trigger price, and will always provide
            the default trigger condition when creating or modifying an Order.
            A special restriction applies when creating a guaranteed Stop Loss Order. In this case the TriggerCondition
            value must either be "DEFAULT", or the "natural" trigger side "DEFAULT" results in. So for a Stop Loss Order for
            a long trade valid values are "DEFAULT" and "BID", and for short trades "DEFAULT" and "ASK" are valid.
        client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
            clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
            your account is associated with MT4."""

    type: Optional[TrailingStopLossOrderRequestType]
    trade_id: Optional[str]
    client_trade_id: Optional[str]
    distance: Optional[str]
    time_in_force: Optional[TrailingStopLossOrderRequestTimeInForce]
    gtd_time: Optional[str]
    trigger_condition: Optional[TrailingStopLossOrderRequestTriggerCondition]
    client_extensions: Optional["ClientExtensions"]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .client_extensions import ClientExtensions

        d = src_dict.copy()
        _type = d.pop("type", None)
        type: Optional[TrailingStopLossOrderRequestType]
        if _type is None:
            type = None
        else:
            type = check_trailing_stop_loss_order_request_type(_type)
        trade_id = d.pop("tradeID", None)
        client_trade_id = d.pop("clientTradeID", None)
        distance = d.pop("distance", None)
        _time_in_force = d.pop("timeInForce", None)
        time_in_force: Optional[TrailingStopLossOrderRequestTimeInForce]
        if isinstance(_time_in_force, Unset):
            time_in_force = None
        else:
            time_in_force = check_trailing_stop_loss_order_request_time_in_force(
                _time_in_force
            )
        gtd_time = d.pop("gtdTime", None)
        _trigger_condition = d.pop("triggerCondition", None)
        trigger_condition: Optional[TrailingStopLossOrderRequestTriggerCondition]
        if isinstance(_trigger_condition, Unset):
            trigger_condition = None
        else:
            trigger_condition = (
                check_trailing_stop_loss_order_request_trigger_condition(
                    _trigger_condition
                )
            )
        _client_extensions = d.pop("clientExtensions", None)
        client_extensions: Optional[ClientExtensions]
        if isinstance(_client_extensions, Unset):
            client_extensions = None
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)
        trailing_stop_loss_order_request = cls(
            type=type,
            trade_id=trade_id,
            client_trade_id=client_trade_id,
            distance=distance,
            time_in_force=time_in_force,
            gtd_time=gtd_time,
            trigger_condition=trigger_condition,
            client_extensions=client_extensions,
        )
        trailing_stop_loss_order_request.additional_properties = d
        return trailing_stop_loss_order_request

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
