from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple
from luna_facilities.core.unit import Unit
from luna_facilities.core.snapshot import Snapshot

@dataclass
class RangeAndComms(Unit):
    name: str = "RangeAndComms"
    capacity_channels: int = 10
    blackout_periods: List[Tuple[float, float]] = field(default_factory=list)
    reservations: List[Dict[str, Any]] = field(default_factory=list)

    def observe(self) -> Snapshot:
        return Snapshot({
            "capacity_channels": self.capacity_channels,
            "blackout_periods": tuple(self.blackout_periods),
            "reservations": tuple(tuple(sorted(r.items())) for r in self.reservations),
        })

    def is_blackout(self, t: float) -> bool:
        return any(a <= t <= b for a, b in self.blackout_periods)
