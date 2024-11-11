from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.liquidity_regeneration_schedule_step import (
        LiquidityRegenerationScheduleStep,
    )


T = TypeVar("T", bound="LiquidityRegenerationSchedule")


@_attrs_define
class LiquidityRegenerationSchedule:
    """A LiquidityRegenerationSchedule indicates how liquidity that is used when filling an Order for an instrument is
    regenerated following the fill.  A liquidity regeneration schedule will be in effect until the timestamp of its
    final step, but may be replaced by a schedule created for an Order of the same instrument that is filled while it is
    still in effect.

        Attributes:
            steps (Union[Unset, List['LiquidityRegenerationScheduleStep']]): The steps in the Liquidity Regeneration
                Schedule
    """

    steps: Union[Unset, List["LiquidityRegenerationScheduleStep"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        steps: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.steps, Unset):
            steps = []
            for steps_item_data in self.steps:
                steps_item = steps_item_data.to_dict()
                steps.append(steps_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if steps is not UNSET:
            field_dict["steps"] = steps

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.liquidity_regeneration_schedule_step import (
            LiquidityRegenerationScheduleStep,
        )

        d = src_dict.copy()
        steps = []
        _steps = d.pop("steps", UNSET)
        for steps_item_data in _steps or []:
            steps_item = LiquidityRegenerationScheduleStep.from_dict(steps_item_data)

            steps.append(steps_item)

        liquidity_regeneration_schedule = cls(
            steps=steps,
        )

        liquidity_regeneration_schedule.additional_properties = d
        return liquidity_regeneration_schedule

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
