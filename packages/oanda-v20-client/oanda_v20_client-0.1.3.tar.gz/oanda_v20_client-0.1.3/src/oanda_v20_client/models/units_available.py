from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.units_available_details import UnitsAvailableDetails


T = TypeVar("T", bound="UnitsAvailable")


@_attrs_define
class UnitsAvailable:
    """Representation of how many units of an Instrument are available to be traded by an Order depending on its
    postionFill option.

        Attributes:
            default (Union[Unset, UnitsAvailableDetails]): Representation of many units of an Instrument are available to be
                traded for both long and short Orders.
            reduce_first (Union[Unset, UnitsAvailableDetails]): Representation of many units of an Instrument are available
                to be traded for both long and short Orders.
            reduce_only (Union[Unset, UnitsAvailableDetails]): Representation of many units of an Instrument are available
                to be traded for both long and short Orders.
            open_only (Union[Unset, UnitsAvailableDetails]): Representation of many units of an Instrument are available to
                be traded for both long and short Orders.
    """

    default: Union[Unset, "UnitsAvailableDetails"] = UNSET
    reduce_first: Union[Unset, "UnitsAvailableDetails"] = UNSET
    reduce_only: Union[Unset, "UnitsAvailableDetails"] = UNSET
    open_only: Union[Unset, "UnitsAvailableDetails"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        default: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.default, Unset):
            default = self.default.to_dict()

        reduce_first: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.reduce_first, Unset):
            reduce_first = self.reduce_first.to_dict()

        reduce_only: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.reduce_only, Unset):
            reduce_only = self.reduce_only.to_dict()

        open_only: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.open_only, Unset):
            open_only = self.open_only.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if default is not UNSET:
            field_dict["default"] = default
        if reduce_first is not UNSET:
            field_dict["reduceFirst"] = reduce_first
        if reduce_only is not UNSET:
            field_dict["reduceOnly"] = reduce_only
        if open_only is not UNSET:
            field_dict["openOnly"] = open_only

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.units_available_details import UnitsAvailableDetails

        d = src_dict.copy()
        _default = d.pop("default", UNSET)
        default: Union[Unset, UnitsAvailableDetails]
        if isinstance(_default, Unset):
            default = UNSET
        else:
            default = UnitsAvailableDetails.from_dict(_default)

        _reduce_first = d.pop("reduceFirst", UNSET)
        reduce_first: Union[Unset, UnitsAvailableDetails]
        if isinstance(_reduce_first, Unset):
            reduce_first = UNSET
        else:
            reduce_first = UnitsAvailableDetails.from_dict(_reduce_first)

        _reduce_only = d.pop("reduceOnly", UNSET)
        reduce_only: Union[Unset, UnitsAvailableDetails]
        if isinstance(_reduce_only, Unset):
            reduce_only = UNSET
        else:
            reduce_only = UnitsAvailableDetails.from_dict(_reduce_only)

        _open_only = d.pop("openOnly", UNSET)
        open_only: Union[Unset, UnitsAvailableDetails]
        if isinstance(_open_only, Unset):
            open_only = UNSET
        else:
            open_only = UnitsAvailableDetails.from_dict(_open_only)

        units_available = cls(
            default=default,
            reduce_first=reduce_first,
            reduce_only=reduce_only,
            open_only=open_only,
        )

        units_available.additional_properties = d
        return units_available

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
