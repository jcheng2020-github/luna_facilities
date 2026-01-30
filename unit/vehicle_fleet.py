from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict
import random

from luna_ops.core.unit import Unit
from luna_ops.core.snapshot import Snapshot
from luna_ops.vehicles.base_vehicle import Vehicle

@dataclass
class VehicleFleet(Unit):
    name: str = "VehicleFleet"
    vehicles: Dict[str, Vehicle] = field(default_factory=dict)

    def observe(self) -> Snapshot:
        return Snapshot({"vehicles": {vid: v.observe() for vid, v in self.vehicles.items()}})

    def step_exogenous(self, dt: float, rng: random.Random) -> None:
        # Optionally: fleet-wide degradation/noise here
        pass
