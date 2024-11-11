from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.client_price_status import check_client_price_status
from ..models.client_price_status import ClientPriceStatus
from typing import Union

if TYPE_CHECKING:
    from ..models.quote_home_conversion_factors import QuoteHomeConversionFactors
    from ..models.price_bucket import PriceBucket
    from ..models.units_available import UnitsAvailable


T = TypeVar("T", bound="ClientPrice")


@_attrs_define
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
            to be traded by an Order depending on its postionFill option.
    """

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
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type

        instrument = self.instrument

        time = self.time

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status

        tradeable = self.tradeable

        bids: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.bids, Unset):
            bids = []
            for bids_item_data in self.bids:
                bids_item = bids_item_data.to_dict()
                bids.append(bids_item)

        asks: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.asks, Unset):
            asks = []
            for asks_item_data in self.asks:
                asks_item = asks_item_data.to_dict()
                asks.append(asks_item)

        closeout_bid = self.closeout_bid

        closeout_ask = self.closeout_ask

        quote_home_conversion_factors: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.quote_home_conversion_factors, Unset):
            quote_home_conversion_factors = self.quote_home_conversion_factors.to_dict()

        units_available: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.units_available, Unset):
            units_available = self.units_available.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if instrument is not UNSET:
            field_dict["instrument"] = instrument
        if time is not UNSET:
            field_dict["time"] = time
        if status is not UNSET:
            field_dict["status"] = status
        if tradeable is not UNSET:
            field_dict["tradeable"] = tradeable
        if bids is not UNSET:
            field_dict["bids"] = bids
        if asks is not UNSET:
            field_dict["asks"] = asks
        if closeout_bid is not UNSET:
            field_dict["closeoutBid"] = closeout_bid
        if closeout_ask is not UNSET:
            field_dict["closeoutAsk"] = closeout_ask
        if quote_home_conversion_factors is not UNSET:
            field_dict["quoteHomeConversionFactors"] = quote_home_conversion_factors
        if units_available is not UNSET:
            field_dict["unitsAvailable"] = units_available

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.quote_home_conversion_factors import QuoteHomeConversionFactors
        from ..models.price_bucket import PriceBucket
        from ..models.units_available import UnitsAvailable

        d = src_dict.copy()
        type = d.pop("type", UNSET)

        instrument = d.pop("instrument", UNSET)

        time = d.pop("time", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, ClientPriceStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = check_client_price_status(_status)

        tradeable = d.pop("tradeable", UNSET)

        bids = []
        _bids = d.pop("bids", UNSET)
        for bids_item_data in _bids or []:
            bids_item = PriceBucket.from_dict(bids_item_data)

            bids.append(bids_item)

        asks = []
        _asks = d.pop("asks", UNSET)
        for asks_item_data in _asks or []:
            asks_item = PriceBucket.from_dict(asks_item_data)

            asks.append(asks_item)

        closeout_bid = d.pop("closeoutBid", UNSET)

        closeout_ask = d.pop("closeoutAsk", UNSET)

        _quote_home_conversion_factors = d.pop("quoteHomeConversionFactors", UNSET)
        quote_home_conversion_factors: Union[Unset, QuoteHomeConversionFactors]
        if isinstance(_quote_home_conversion_factors, Unset):
            quote_home_conversion_factors = UNSET
        else:
            quote_home_conversion_factors = QuoteHomeConversionFactors.from_dict(
                _quote_home_conversion_factors
            )

        _units_available = d.pop("unitsAvailable", UNSET)
        units_available: Union[Unset, UnitsAvailable]
        if isinstance(_units_available, Unset):
            units_available = UNSET
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
