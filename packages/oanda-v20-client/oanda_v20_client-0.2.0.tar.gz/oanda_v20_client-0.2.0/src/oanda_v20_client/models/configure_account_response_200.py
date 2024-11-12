from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.client_configure_transaction import ClientConfigureTransaction


T = TypeVar("T", bound="ConfigureAccountResponse200")


@_attrs_define
class ConfigureAccountResponse200:
    """
    Attributes:
        client_configure_transaction (Union[Unset, ClientConfigureTransaction]): A ClientConfigureTransaction represents
            the configuration of an Account by a client.
        last_transaction_id (Union[Unset, str]): The ID of the last Transaction created for the Account.
    """

    client_configure_transaction: Union[Unset, "ClientConfigureTransaction"] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        client_configure_transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.client_configure_transaction, Unset):
            client_configure_transaction = self.client_configure_transaction.to_dict()

        last_transaction_id = self.last_transaction_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if client_configure_transaction is not UNSET:
            field_dict["clientConfigureTransaction"] = client_configure_transaction
        if last_transaction_id is not UNSET:
            field_dict["lastTransactionID"] = last_transaction_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.client_configure_transaction import ClientConfigureTransaction

        d = src_dict.copy()
        _client_configure_transaction = d.pop("clientConfigureTransaction", UNSET)
        client_configure_transaction: Union[Unset, ClientConfigureTransaction]
        if isinstance(_client_configure_transaction, Unset):
            client_configure_transaction = UNSET
        else:
            client_configure_transaction = ClientConfigureTransaction.from_dict(
                _client_configure_transaction
            )

        last_transaction_id = d.pop("lastTransactionID", UNSET)

        configure_account_response_200 = cls(
            client_configure_transaction=client_configure_transaction,
            last_transaction_id=last_transaction_id,
        )

        configure_account_response_200.additional_properties = d
        return configure_account_response_200

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
