from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.order_book import OrderBook


T = TypeVar("T", bound="GetInstrumentsInstrumentOrderBookResponse200")


@_attrs_define
class GetInstrumentsInstrumentOrderBookResponse200:
    """
    Attributes:
        order_book (Union[Unset, OrderBook]): The representation of an instrument's order book at a point in time
    """

    order_book: Union[Unset, "OrderBook"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        order_book: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.order_book, Unset):
            order_book = self.order_book.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if order_book is not UNSET:
            field_dict["orderBook"] = order_book

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.order_book import OrderBook

        d = src_dict.copy()
        _order_book = d.pop("orderBook", UNSET)
        order_book: Union[Unset, OrderBook]
        if isinstance(_order_book, Unset):
            order_book = UNSET
        else:
            order_book = OrderBook.from_dict(_order_book)

        get_instruments_instrument_order_book_response_200 = cls(
            order_book=order_book,
        )

        get_instruments_instrument_order_book_response_200.additional_properties = d
        return get_instruments_instrument_order_book_response_200

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
