from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.price_bucket import PriceBucket


T = TypeVar("T", bound="Price")


@_attrs_define
class Price:
    """The Price representation

    Attributes:
        instrument (Union[Unset, str]): The Price's Instrument.
        tradeable (Union[Unset, bool]): Flag indicating if the Price is tradeable or not
        timestamp (Union[Unset, str]): The date/time when the Price was created.
        base_bid (Union[Unset, str]): The base bid price as calculated by pricing.
        base_ask (Union[Unset, str]): The base ask price as calculated by pricing.
        bids (Union[Unset, List['PriceBucket']]): The list of prices and liquidity available on the Instrument's bid
            side. It is possible for this list to be empty if there is no bid liquidity currently available for the
            Instrument in the Account.
        asks (Union[Unset, List['PriceBucket']]): The list of prices and liquidity available on the Instrument's ask
            side. It is possible for this list to be empty if there is no ask liquidity currently available for the
            Instrument in the Account.
        closeout_bid (Union[Unset, str]): The closeout bid price. This price is used when a bid is required to closeout
            a Position (margin closeout or manual) yet there is no bid liquidity. The closeout bid is never used to open a
            new position.
        closeout_ask (Union[Unset, str]): The closeout ask price. This price is used when an ask is required to closeout
            a Position (margin closeout or manual) yet there is no ask liquidity. The closeout ask is never used to open a
            new position.
    """

    instrument: Union[Unset, str] = UNSET
    tradeable: Union[Unset, bool] = UNSET
    timestamp: Union[Unset, str] = UNSET
    base_bid: Union[Unset, str] = UNSET
    base_ask: Union[Unset, str] = UNSET
    bids: Union[Unset, List["PriceBucket"]] = UNSET
    asks: Union[Unset, List["PriceBucket"]] = UNSET
    closeout_bid: Union[Unset, str] = UNSET
    closeout_ask: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        instrument = self.instrument

        tradeable = self.tradeable

        timestamp = self.timestamp

        base_bid = self.base_bid

        base_ask = self.base_ask

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

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if instrument is not UNSET:
            field_dict["instrument"] = instrument
        if tradeable is not UNSET:
            field_dict["tradeable"] = tradeable
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if base_bid is not UNSET:
            field_dict["baseBid"] = base_bid
        if base_ask is not UNSET:
            field_dict["baseAsk"] = base_ask
        if bids is not UNSET:
            field_dict["bids"] = bids
        if asks is not UNSET:
            field_dict["asks"] = asks
        if closeout_bid is not UNSET:
            field_dict["closeoutBid"] = closeout_bid
        if closeout_ask is not UNSET:
            field_dict["closeoutAsk"] = closeout_ask

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.price_bucket import PriceBucket

        d = src_dict.copy()
        instrument = d.pop("instrument", UNSET)

        tradeable = d.pop("tradeable", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        base_bid = d.pop("baseBid", UNSET)

        base_ask = d.pop("baseAsk", UNSET)

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

        price = cls(
            instrument=instrument,
            tradeable=tradeable,
            timestamp=timestamp,
            base_bid=base_bid,
            base_ask=base_ask,
            bids=bids,
            asks=asks,
            closeout_bid=closeout_bid,
            closeout_ask=closeout_ask,
        )

        price.additional_properties = d
        return price

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
