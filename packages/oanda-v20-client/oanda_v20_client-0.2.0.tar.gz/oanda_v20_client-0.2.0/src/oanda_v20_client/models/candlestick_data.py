from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="CandlestickData")


@_attrs_define
class CandlestickData:
    """The price data (open, high, low, close) for the Candlestick representation.

    Attributes:
        o (Union[Unset, str]): The first (open) price in the time-range represented by the candlestick.
        h (Union[Unset, str]): The highest price in the time-range represented by the candlestick.
        l (Union[Unset, str]): The lowest price in the time-range represented by the candlestick.
        c (Union[Unset, str]): The last (closing) price in the time-range represented by the candlestick.
    """

    o: Union[Unset, str] = UNSET
    h: Union[Unset, str] = UNSET
    l: Union[Unset, str] = UNSET
    c: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        o = self.o

        h = self.h

        l = self.l

        c = self.c

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if o is not UNSET:
            field_dict["o"] = o
        if h is not UNSET:
            field_dict["h"] = h
        if l is not UNSET:
            field_dict["l"] = l
        if c is not UNSET:
            field_dict["c"] = c

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        o = d.pop("o", UNSET)

        h = d.pop("h", UNSET)

        l = d.pop("l", UNSET)

        c = d.pop("c", UNSET)

        candlestick_data = cls(
            o=o,
            h=h,
            l=l,
            c=c,
        )

        candlestick_data.additional_properties = d
        return candlestick_data

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
