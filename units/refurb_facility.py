from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List
import random
from luna_facilities.core.unit import Unit
from luna_facilities.core.snapshot import Snapshot

@dataclass
class RefurbFacility(Unit):
    name: str = "RefurbFacility"
    bays: int = 4
    queue: List[str] = field(default_factory=list)
    in_service: Dict[str, float] = field(default_factory=dict)  # vehicle_id -> remaining_hours

    def observe(self) -> Snapshot:
        return Snapshot({
            "bays": self.bays,
            "queue": tuple(self.queue),
            "in_service": self.in_service.copy(),
        })

    def start(self, vehicle_id: str, duration_hours: float) -> bool:
        if len(self.in_service) >= self.bays:
            self.queue.append(vehicle_id)
            return False
        self.in_service[vehicle_id] = max(0.0, duration_hours)
        return True

    def step_exogenous(self, dt: float, rng: random.Random) -> None:
        done = []
        for vid in list(self.in_service.keys()):
            self.in_service[vid] -= dt
            if self.in_service[vid] <= 0:
                done.append(vid)
                del self.in_service[vid]

        while self.queue and len(self.in_service) < self.bays:
            next_vid = self.queue.pop(0)
            self.in_service[next_vid] = 24.0  # placeholder default
