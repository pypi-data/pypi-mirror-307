from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .client_extensions import ClientExtensions
from .stop_loss_order_request_time_in_force import StopLossOrderRequestTimeInForce
from .stop_loss_order_request_trigger_condition import (
    StopLossOrderRequestTriggerCondition,
)
from .stop_loss_order_request_type import StopLossOrderRequestType
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="StopLossOrderRequest")


@dataclasses.dataclass
class StopLossOrderRequest:
    """A StopLossOrderRequest specifies the parameters that may be set when creating a Stop Loss Order. Only one of the
    price and distance fields may be specified.

        Attributes:
            type (Union[Unset, StopLossOrderRequestType]): The type of the Order to Create. Must be set to "STOP_LOSS" when
                creating a Stop Loss Order.
            trade_id (Union[Unset, str]): The ID of the Trade to close when the price threshold is breached.
            client_trade_id (Union[Unset, str]): The client ID of the Trade to be closed when the price threshold is
                breached.
            price (Union[Unset, str]): The price threshold specified for the Stop Loss Order. If the guaranteed flag is
                false, the associated Trade will be closed by a market price that is equal to or worse than this threshold. If
                the flag is true the associated Trade will be closed at this price.
            distance (Union[Unset, str]): Specifies the distance (in price units) from the Account's current price to use as
                the Stop Loss Order price. If the Trade is short the Instrument's bid price is used, and for long Trades the ask
                is used.
            time_in_force (Union[Unset, StopLossOrderRequestTimeInForce]): The time-in-force requested for the StopLoss
                Order. Restricted to "GTC", "GFD" and "GTD" for StopLoss Orders.
            gtd_time (Union[Unset, str]): The date/time when the StopLoss Order will be cancelled if its timeInForce is
                "GTD".
            trigger_condition (Union[Unset, StopLossOrderRequestTriggerCondition]): Specification of which price component
                should be used when determining if an Order should be triggered and filled. This allows Orders to be triggered
                based on the bid, ask, mid, default (ask for buy, bid for sell) or inverse (ask for sell, bid for buy) price
                depending on the desired behaviour. Orders are always filled using their default price component.
                This feature is only provided through the REST API. Clients who choose to specify a non-default trigger
                condition will not see it reflected in any of OANDA's proprietary or partner trading platforms, their
                transaction history or their account statements. OANDA platforms always assume that an Order's trigger condition
                is set to the default value when indicating the distance from an Order's trigger price, and will always provide
                the default trigger condition when creating or modifying an Order.
                A special restriction applies when creating a guaranteed Stop Loss Order. In this case the TriggerCondition
                value must either be "DEFAULT", or the "natural" trigger side "DEFAULT" results in. So for a Stop Loss Order for
                a long trade valid values are "DEFAULT" and "BID", and for short trades "DEFAULT" and "ASK" are valid.
            guaranteed (Union[Unset, bool]): Flag indicating that the Stop Loss Order is guaranteed. The default value
                depends on the GuaranteedStopLossOrderMode of the account, if it is REQUIRED, the default will be true, for
                DISABLED or ENABLED the default is false.
            client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
                clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
                your account is associated with MT4."""

    type: Union[Unset, StopLossOrderRequestType] = UNSET
    trade_id: Union[Unset, str] = UNSET
    client_trade_id: Union[Unset, str] = UNSET
    price: Union[Unset, str] = UNSET
    distance: Union[Unset, str] = UNSET
    time_in_force: Union[Unset, StopLossOrderRequestTimeInForce] = UNSET
    gtd_time: Union[Unset, str] = UNSET
    trigger_condition: Union[Unset, StopLossOrderRequestTriggerCondition] = UNSET
    guaranteed: Union[Unset, bool] = UNSET
    client_extensions: Union[Unset, "ClientExtensions"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StopLossOrderRequest":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
