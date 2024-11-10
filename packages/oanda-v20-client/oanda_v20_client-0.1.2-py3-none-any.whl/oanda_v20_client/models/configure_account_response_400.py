from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.client_configure_reject_transaction import (
        ClientConfigureRejectTransaction,
    )


T = TypeVar("T", bound="ConfigureAccountResponse400")


@_attrs_define
class ConfigureAccountResponse400:
    """
    Attributes:
        client_configure_reject_transaction (Union[Unset, ClientConfigureRejectTransaction]): A
            ClientConfigureRejectTransaction represents the reject of configuration of an Account by a client.
        last_transaction_id (Union[Unset, str]): The ID of the last Transaction created for the Account.
        error_code (Union[Unset, str]): The code of the error that has occurred. This field may not be returned for some
            errors.
        error_message (Union[Unset, str]): The human-readable description of the error that has occurred.
    """

    client_configure_reject_transaction: Union[
        Unset, "ClientConfigureRejectTransaction"
    ] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    error_code: Union[Unset, str] = UNSET
    error_message: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        client_configure_reject_transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.client_configure_reject_transaction, Unset):
            client_configure_reject_transaction = (
                self.client_configure_reject_transaction.to_dict()
            )

        last_transaction_id = self.last_transaction_id

        error_code = self.error_code

        error_message = self.error_message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if client_configure_reject_transaction is not UNSET:
            field_dict["clientConfigureRejectTransaction"] = (
                client_configure_reject_transaction
            )
        if last_transaction_id is not UNSET:
            field_dict["lastTransactionID"] = last_transaction_id
        if error_code is not UNSET:
            field_dict["errorCode"] = error_code
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.client_configure_reject_transaction import (
            ClientConfigureRejectTransaction,
        )

        d = src_dict.copy()
        _client_configure_reject_transaction = d.pop(
            "clientConfigureRejectTransaction", UNSET
        )
        client_configure_reject_transaction: Union[
            Unset, ClientConfigureRejectTransaction
        ]
        if isinstance(_client_configure_reject_transaction, Unset):
            client_configure_reject_transaction = UNSET
        else:
            client_configure_reject_transaction = (
                ClientConfigureRejectTransaction.from_dict(
                    _client_configure_reject_transaction
                )
            )

        last_transaction_id = d.pop("lastTransactionID", UNSET)

        error_code = d.pop("errorCode", UNSET)

        error_message = d.pop("errorMessage", UNSET)

        configure_account_response_400 = cls(
            client_configure_reject_transaction=client_configure_reject_transaction,
            last_transaction_id=last_transaction_id,
            error_code=error_code,
            error_message=error_message,
        )

        configure_account_response_400.additional_properties = d
        return configure_account_response_400

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
