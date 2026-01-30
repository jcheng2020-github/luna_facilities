from __future__ import annotations
from dataclasses import dataclass
from luna_ops.core.unit import Unit
from luna_ops.core.snapshot import Snapshot

@dataclass
class SurfacePowerSystem(Unit):
    name: str = "SurfacePowerSystem"

    available_kw: float = 500.0
    battery_kwh: float = 2000.0
    battery_cap_kwh: float = 4000.0

    def observe(self) -> Snapshot:
        return Snapshot(self.__dict__.copy())

    def allocate_kw(self, kw: float) -> float:
        used = min(self.available_kw, max(0.0, kw))
        self.available_kw -= used
        return used
