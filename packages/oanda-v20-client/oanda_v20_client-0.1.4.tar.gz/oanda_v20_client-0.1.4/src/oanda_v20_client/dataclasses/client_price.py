from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .client_price_status import ClientPriceStatus
from .price_bucket import PriceBucket
from .quote_home_conversion_factors import QuoteHomeConversionFactors
from .units_available import UnitsAvailable
from typing import List, TypeVar, Union

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

    type: Union[Unset, str] = UNSET
    instrument: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    status: Union[Unset, ClientPriceStatus] = UNSET
    tradeable: Union[Unset, bool] = UNSET
    bids: Union[Unset, List["PriceBucket"]] = UNSET
    asks: Union[Unset, List["PriceBucket"]] = UNSET
    closeout_bid: Union[Unset, str] = UNSET
    closeout_ask: Union[Unset, str] = UNSET
    quote_home_conversion_factors: Union[Unset, "QuoteHomeConversionFactors"] = UNSET
    units_available: Union[Unset, "UnitsAvailable"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClientPrice":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
