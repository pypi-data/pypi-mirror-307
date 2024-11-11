from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.get_instrument_candles_response_200_granularity import (
    check_get_instrument_candles_response_200_granularity,
)
from ..models.get_instrument_candles_response_200_granularity import (
    GetInstrumentCandlesResponse200Granularity,
)
from typing import Union

if TYPE_CHECKING:
    from ..models.candlestick import Candlestick


T = TypeVar("T", bound="GetInstrumentCandlesResponse200")


@_attrs_define
class GetInstrumentCandlesResponse200:
    """
    Attributes:
        instrument (Union[Unset, str]): The instrument whose Prices are represented by the candlesticks.
        granularity (Union[Unset, GetInstrumentCandlesResponse200Granularity]): The granularity of the candlesticks
            provided.
        candles (Union[Unset, List['Candlestick']]): The list of candlesticks that satisfy the request.
    """

    instrument: Union[Unset, str] = UNSET
    granularity: Union[Unset, GetInstrumentCandlesResponse200Granularity] = UNSET
    candles: Union[Unset, List["Candlestick"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        instrument = self.instrument

        granularity: Union[Unset, str] = UNSET
        if not isinstance(self.granularity, Unset):
            granularity = self.granularity

        candles: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.candles, Unset):
            candles = []
            for candles_item_data in self.candles:
                candles_item = candles_item_data.to_dict()
                candles.append(candles_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if instrument is not UNSET:
            field_dict["instrument"] = instrument
        if granularity is not UNSET:
            field_dict["granularity"] = granularity
        if candles is not UNSET:
            field_dict["candles"] = candles

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.candlestick import Candlestick

        d = src_dict.copy()
        instrument = d.pop("instrument", UNSET)

        _granularity = d.pop("granularity", UNSET)
        granularity: Union[Unset, GetInstrumentCandlesResponse200Granularity]
        if isinstance(_granularity, Unset):
            granularity = UNSET
        else:
            granularity = check_get_instrument_candles_response_200_granularity(
                _granularity
            )

        candles = []
        _candles = d.pop("candles", UNSET)
        for candles_item_data in _candles or []:
            candles_item = Candlestick.from_dict(candles_item_data)

            candles.append(candles_item)

        get_instrument_candles_response_200 = cls(
            instrument=instrument,
            granularity=granularity,
            candles=candles,
        )

        get_instrument_candles_response_200.additional_properties = d
        return get_instrument_candles_response_200

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
