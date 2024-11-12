from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="TransactionHeartbeat")


@_attrs_define
class TransactionHeartbeat:
    """A TransactionHeartbeat object is injected into the Transaction stream to ensure that the HTTP connection remains
    active.

        Attributes:
            type (Union[Unset, str]): The string "HEARTBEAT"
            last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account
            time (Union[Unset, str]): The date/time when the TransactionHeartbeat was created.
    """

    type: Union[Unset, str] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type

        last_transaction_id = self.last_transaction_id

        time = self.time

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if last_transaction_id is not UNSET:
            field_dict["lastTransactionID"] = last_transaction_id
        if time is not UNSET:
            field_dict["time"] = time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type", UNSET)

        last_transaction_id = d.pop("lastTransactionID", UNSET)

        time = d.pop("time", UNSET)

        transaction_heartbeat = cls(
            type=type,
            last_transaction_id=last_transaction_id,
            time=time,
        )

        transaction_heartbeat.additional_properties = d
        return transaction_heartbeat

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
