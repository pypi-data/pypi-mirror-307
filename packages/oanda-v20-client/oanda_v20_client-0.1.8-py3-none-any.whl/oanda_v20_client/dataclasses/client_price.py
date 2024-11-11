from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_price_status import ClientPriceStatus
from .client_price_status import check_client_price_status
from .price_bucket import PriceBucket
from .quote_home_conversion_factors import QuoteHomeConversionFactors
from .units_available import UnitsAvailable
from types import Unset
from typing import List, Optional, Type, TypeVar

T = TypeVar("T", bound="ClientPrice")


@dataclasses.dataclass
class ClientPrice:
    """The specification of an Account-specific Price.

    Attributes:
        type (Union[Unset, str]): The string "PRICE". Used to identify the a Price object when found in a stream.
        instrument (Union[Unset, str]): The Price's Instrument.
        time (Union[Unset, str]): The date/time when the Price was created
        status (Union[Unset, ClientPriceStatus]): The status of the Price.
        tradeable (Union[Unset, bool]): Flag indicating if the Price is tradeable or not
        bids (Union[Unset, List['PriceBucket']]): The list of prices and liquidity available on the Instrument's bid
            side. It is possible for this list to be empty if there is no bid liquidity currently available for the
            Instrument in the Account.
        asks (Union[Unset, List['PriceBucket']]): The list of prices and liquidity available on the Instrument's ask
            side. It is possible for this list to be empty if there is no ask liquidity currently available for the
            Instrument in the Account.
        closeout_bid (Union[Unset, str]): The closeout bid Price. This Price is used when a bid is required to closeout
            a Position (margin closeout or manual) yet there is no bid liquidity. The closeout bid is never used to open a
            new position.
        closeout_ask (Union[Unset, str]): The closeout ask Price. This Price is used when a ask is required to closeout
            a Position (margin closeout or manual) yet there is no ask liquidity. The closeout ask is never used to open a
            new position.
        quote_home_conversion_factors (Union[Unset, QuoteHomeConversionFactors]): QuoteHomeConversionFactors represents
            the factors that can be used used to convert quantities of a Price's Instrument's quote currency into the
            Account's home currency.
        units_available (Union[Unset, UnitsAvailable]): Representation of how many units of an Instrument are available
            to be traded by an Order depending on its postionFill option."""

    type: Optional[str]
    instrument: Optional[str]
    time: Optional[str]
    status: Optional[ClientPriceStatus]
    tradeable: Optional[bool]
    bids: Optional[List["PriceBucket"]]
    asks: Optional[List["PriceBucket"]]
    closeout_bid: Optional[str]
    closeout_ask: Optional[str]
    quote_home_conversion_factors: Optional["QuoteHomeConversionFactors"]
    units_available: Optional["UnitsAvailable"]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .units_available import UnitsAvailable
        from .quote_home_conversion_factors import QuoteHomeConversionFactors
        from .price_bucket import PriceBucket

        d = src_dict.copy()
        type = d.pop("type", None)
        instrument = d.pop("instrument", None)
        time = d.pop("time", None)
        _status = d.pop("status", None)
        status: Optional[ClientPriceStatus]
        if isinstance(_status, Unset):
            status = None
        else:
            status = check_client_price_status(_status)
        tradeable = d.pop("tradeable", None)
        bids = []
        _bids = d.pop("bids", None)
        for bids_item_data in _bids or []:
            bids_item = PriceBucket.from_dict(bids_item_data)
            bids.append(bids_item)
        asks = []
        _asks = d.pop("asks", None)
        for asks_item_data in _asks or []:
            asks_item = PriceBucket.from_dict(asks_item_data)
            asks.append(asks_item)
        closeout_bid = d.pop("closeoutBid", None)
        closeout_ask = d.pop("closeoutAsk", None)
        _quote_home_conversion_factors = d.pop("quoteHomeConversionFactors", None)
        quote_home_conversion_factors: Optional[QuoteHomeConversionFactors]
        if isinstance(_quote_home_conversion_factors, Unset):
            quote_home_conversion_factors = None
        else:
            quote_home_conversion_factors = QuoteHomeConversionFactors.from_dict(
                _quote_home_conversion_factors
            )
        _units_available = d.pop("unitsAvailable", None)
        units_available: Optional[UnitsAvailable]
        if isinstance(_units_available, Unset):
            units_available = None
        else:
            units_available = UnitsAvailable.from_dict(_units_available)
        client_price = cls(
            type=type,
            instrument=instrument,
            time=time,
            status=status,
            tradeable=tradeable,
            bids=bids,
            asks=asks,
            closeout_bid=closeout_bid,
            closeout_ask=closeout_ask,
            quote_home_conversion_factors=quote_home_conversion_factors,
            units_available=units_available,
        )
        client_price.additional_properties = d
        return client_price

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
