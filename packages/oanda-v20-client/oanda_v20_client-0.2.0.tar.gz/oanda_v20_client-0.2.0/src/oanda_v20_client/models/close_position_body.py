from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.client_extensions import ClientExtensions


T = TypeVar("T", bound="ClosePositionBody")


@_attrs_define
class ClosePositionBody:
    """
    Attributes:
        long_units (Union[Unset, str]): Indication of how much of the long Position to closeout. Either the string
            "ALL", the string "NONE", or a DecimalNumber representing how many units of the long position to close using a
            PositionCloseout MarketOrder. The units specified must always be positive.
        long_client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
            clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
            your account is associated with MT4.
        short_units (Union[Unset, str]): Indication of how much of the short Position to closeout. Either the string
            "ALL", the string "NONE", or a DecimalNumber representing how many units of the short position to close using a
            PositionCloseout MarketOrder. The units specified must always be positive.
        short_client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
            clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
            your account is associated with MT4.
    """

    long_units: Union[Unset, str] = UNSET
    long_client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    short_units: Union[Unset, str] = UNSET
    short_client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        long_units = self.long_units

        long_client_extensions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.long_client_extensions, Unset):
            long_client_extensions = self.long_client_extensions.to_dict()

        short_units = self.short_units

        short_client_extensions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.short_client_extensions, Unset):
            short_client_extensions = self.short_client_extensions.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if long_units is not UNSET:
            field_dict["longUnits"] = long_units
        if long_client_extensions is not UNSET:
            field_dict["longClientExtensions"] = long_client_extensions
        if short_units is not UNSET:
            field_dict["shortUnits"] = short_units
        if short_client_extensions is not UNSET:
            field_dict["shortClientExtensions"] = short_client_extensions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.client_extensions import ClientExtensions

        d = src_dict.copy()
        long_units = d.pop("longUnits", UNSET)

        _long_client_extensions = d.pop("longClientExtensions", UNSET)
        long_client_extensions: Union[Unset, ClientExtensions]
        if isinstance(_long_client_extensions, Unset):
            long_client_extensions = UNSET
        else:
            long_client_extensions = ClientExtensions.from_dict(_long_client_extensions)

        short_units = d.pop("shortUnits", UNSET)

        _short_client_extensions = d.pop("shortClientExtensions", UNSET)
        short_client_extensions: Union[Unset, ClientExtensions]
        if isinstance(_short_client_extensions, Unset):
            short_client_extensions = UNSET
        else:
            short_client_extensions = ClientExtensions.from_dict(
                _short_client_extensions
            )

        close_position_body = cls(
            long_units=long_units,
            long_client_extensions=long_client_extensions,
            short_units=short_units,
            short_client_extensions=short_client_extensions,
        )

        close_position_body.additional_properties = d
        return close_position_body

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
