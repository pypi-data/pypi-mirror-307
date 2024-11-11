from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.candlestick_data import CandlestickData


T = TypeVar("T", bound="Candlestick")


@_attrs_define
class Candlestick:
    """The Candlestick representation

    Attributes:
        time (Union[Unset, str]): The start time of the candlestick
        bid (Union[Unset, CandlestickData]): The price data (open, high, low, close) for the Candlestick representation.
        ask (Union[Unset, CandlestickData]): The price data (open, high, low, close) for the Candlestick representation.
        mid (Union[Unset, CandlestickData]): The price data (open, high, low, close) for the Candlestick representation.
        volume (Union[Unset, int]): The number of prices created during the time-range represented by the candlestick.
        complete (Union[Unset, bool]): A flag indicating if the candlestick is complete. A complete candlestick is one
            whose ending time is not in the future.
    """

    time: Union[Unset, str] = UNSET
    bid: Union[Unset, "CandlestickData"] = UNSET
    ask: Union[Unset, "CandlestickData"] = UNSET
    mid: Union[Unset, "CandlestickData"] = UNSET
    volume: Union[Unset, int] = UNSET
    complete: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        time = self.time

        bid: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.bid, Unset):
            bid = self.bid.to_dict()

        ask: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.ask, Unset):
            ask = self.ask.to_dict()

        mid: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.mid, Unset):
            mid = self.mid.to_dict()

        volume = self.volume

        complete = self.complete

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if time is not UNSET:
            field_dict["time"] = time
        if bid is not UNSET:
            field_dict["bid"] = bid
        if ask is not UNSET:
            field_dict["ask"] = ask
        if mid is not UNSET:
            field_dict["mid"] = mid
        if volume is not UNSET:
            field_dict["volume"] = volume
        if complete is not UNSET:
            field_dict["complete"] = complete

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.candlestick_data import CandlestickData

        d = src_dict.copy()
        time = d.pop("time", UNSET)

        _bid = d.pop("bid", UNSET)
        bid: Union[Unset, CandlestickData]
        if isinstance(_bid, Unset):
            bid = UNSET
        else:
            bid = CandlestickData.from_dict(_bid)

        _ask = d.pop("ask", UNSET)
        ask: Union[Unset, CandlestickData]
        if isinstance(_ask, Unset):
            ask = UNSET
        else:
            ask = CandlestickData.from_dict(_ask)

        _mid = d.pop("mid", UNSET)
        mid: Union[Unset, CandlestickData]
        if isinstance(_mid, Unset):
            mid = UNSET
        else:
            mid = CandlestickData.from_dict(_mid)

        volume = d.pop("volume", UNSET)

        complete = d.pop("complete", UNSET)

        candlestick = cls(
            time=time,
            bid=bid,
            ask=ask,
            mid=mid,
            volume=volume,
            complete=complete,
        )

        candlestick.additional_properties = d
        return candlestick

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
