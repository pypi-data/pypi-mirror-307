from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.position_book import PositionBook


T = TypeVar("T", bound="GetInstrumentsInstrumentPositionBookResponse200")


@_attrs_define
class GetInstrumentsInstrumentPositionBookResponse200:
    """
    Attributes:
        position_book (Union[Unset, PositionBook]): The representation of an instrument's position book at a point in
            time
    """

    position_book: Union[Unset, "PositionBook"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        position_book: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.position_book, Unset):
            position_book = self.position_book.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if position_book is not UNSET:
            field_dict["positionBook"] = position_book

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.position_book import PositionBook

        d = src_dict.copy()
        _position_book = d.pop("positionBook", UNSET)
        position_book: Union[Unset, PositionBook]
        if isinstance(_position_book, Unset):
            position_book = UNSET
        else:
            position_book = PositionBook.from_dict(_position_book)

        get_instruments_instrument_position_book_response_200 = cls(
            position_book=position_book,
        )

        get_instruments_instrument_position_book_response_200.additional_properties = d
        return get_instruments_instrument_position_book_response_200

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
