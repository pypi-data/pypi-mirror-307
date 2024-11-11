from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .liquidity_regeneration_schedule_step import LiquidityRegenerationScheduleStep
from typing import List, Optional, Type, TypeVar

T = TypeVar("T", bound="LiquidityRegenerationSchedule")


@dataclasses.dataclass
class LiquidityRegenerationSchedule:
    """A LiquidityRegenerationSchedule indicates how liquidity that is used when filling an Order for an instrument is
    regenerated following the fill.  A liquidity regeneration schedule will be in effect until the timestamp of its
    final step, but may be replaced by a schedule created for an Order of the same instrument that is filled while it is
    still in effect.

        Attributes:
            steps (Union[Unset, List['LiquidityRegenerationScheduleStep']]): The steps in the Liquidity Regeneration
                Schedule"""

    steps: Optional[List["LiquidityRegenerationScheduleStep"]]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .liquidity_regeneration_schedule_step import (
            LiquidityRegenerationScheduleStep,
        )

        d = src_dict.copy()
        steps = []
        _steps = d.pop("steps", None)
        for steps_item_data in _steps or []:
            steps_item = LiquidityRegenerationScheduleStep.from_dict(steps_item_data)
            steps.append(steps_item)
        liquidity_regeneration_schedule = cls(steps=steps)
        liquidity_regeneration_schedule.additional_properties = d
        return liquidity_regeneration_schedule

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
