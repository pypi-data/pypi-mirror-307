from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.instrument import Instrument


T = TypeVar("T", bound="GetAccountInstrumentsResponse200")


@_attrs_define
class GetAccountInstrumentsResponse200:
    """
    Attributes:
        instruments (Union[Unset, List['Instrument']]): The requested list of instruments.
        last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account.
    """

    instruments: Union[Unset, List["Instrument"]] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        instruments: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.instruments, Unset):
            instruments = []
            for instruments_item_data in self.instruments:
                instruments_item = instruments_item_data.to_dict()
                instruments.append(instruments_item)

        last_transaction_id = self.last_transaction_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if instruments is not UNSET:
            field_dict["instruments"] = instruments
        if last_transaction_id is not UNSET:
            field_dict["lastTransactionID"] = last_transaction_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.instrument import Instrument

        d = src_dict.copy()
        instruments = []
        _instruments = d.pop("instruments", UNSET)
        for instruments_item_data in _instruments or []:
            instruments_item = Instrument.from_dict(instruments_item_data)

            instruments.append(instruments_item)

        last_transaction_id = d.pop("lastTransactionID", UNSET)

        get_account_instruments_response_200 = cls(
            instruments=instruments,
            last_transaction_id=last_transaction_id,
        )

        get_account_instruments_response_200.additional_properties = d
        return get_account_instruments_response_200

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
