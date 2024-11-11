from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.open_trade_financing import OpenTradeFinancing


T = TypeVar("T", bound="PositionFinancing")


@_attrs_define
class PositionFinancing:
    """OpenTradeFinancing is used to pay/collect daily financing charge for a Position within an Account

    Attributes:
        instrument (Union[Unset, str]): The instrument of the Position that financing is being paid/collected for.
        financing (Union[Unset, str]): The amount of financing paid/collected for the Position.
        open_trade_financings (Union[Unset, List['OpenTradeFinancing']]): The financing paid/collecte for each open
            Trade within the Position.
    """

    instrument: Union[Unset, str] = UNSET
    financing: Union[Unset, str] = UNSET
    open_trade_financings: Union[Unset, List["OpenTradeFinancing"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        instrument = self.instrument

        financing = self.financing

        open_trade_financings: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.open_trade_financings, Unset):
            open_trade_financings = []
            for open_trade_financings_item_data in self.open_trade_financings:
                open_trade_financings_item = open_trade_financings_item_data.to_dict()
                open_trade_financings.append(open_trade_financings_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if instrument is not UNSET:
            field_dict["instrument"] = instrument
        if financing is not UNSET:
            field_dict["financing"] = financing
        if open_trade_financings is not UNSET:
            field_dict["openTradeFinancings"] = open_trade_financings

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.open_trade_financing import OpenTradeFinancing

        d = src_dict.copy()
        instrument = d.pop("instrument", UNSET)

        financing = d.pop("financing", UNSET)

        open_trade_financings = []
        _open_trade_financings = d.pop("openTradeFinancings", UNSET)
        for open_trade_financings_item_data in _open_trade_financings or []:
            open_trade_financings_item = OpenTradeFinancing.from_dict(
                open_trade_financings_item_data
            )

            open_trade_financings.append(open_trade_financings_item)

        position_financing = cls(
            instrument=instrument,
            financing=financing,
            open_trade_financings=open_trade_financings,
        )

        position_financing.additional_properties = d
        return position_financing

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
