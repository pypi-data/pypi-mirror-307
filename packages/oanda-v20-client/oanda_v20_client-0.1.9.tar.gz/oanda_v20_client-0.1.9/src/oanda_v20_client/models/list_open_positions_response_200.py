from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.position import Position


T = TypeVar("T", bound="ListOpenPositionsResponse200")


@_attrs_define
class ListOpenPositionsResponse200:
    """
    Attributes:
        positions (Union[Unset, List['Position']]): The list of open Positions in the Account.
        last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account
    """

    positions: Union[Unset, List["Position"]] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        positions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.positions, Unset):
            positions = []
            for positions_item_data in self.positions:
                positions_item = positions_item_data.to_dict()
                positions.append(positions_item)

        last_transaction_id = self.last_transaction_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if positions is not UNSET:
            field_dict["positions"] = positions
        if last_transaction_id is not UNSET:
            field_dict["lastTransactionID"] = last_transaction_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.position import Position

        d = src_dict.copy()
        positions = []
        _positions = d.pop("positions", UNSET)
        for positions_item_data in _positions or []:
            positions_item = Position.from_dict(positions_item_data)

            positions.append(positions_item)

        last_transaction_id = d.pop("lastTransactionID", UNSET)

        list_open_positions_response_200 = cls(
            positions=positions,
            last_transaction_id=last_transaction_id,
        )

        list_open_positions_response_200.additional_properties = d
        return list_open_positions_response_200

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
