from __future__ import annotations
from dataclasses import dataclass
import random
from luna_ops.core.unit import Unit
from luna_ops.core.snapshot import Snapshot

@dataclass
class MissionClock(Unit):
    name: str = "MissionClock"
    t: float = 0.0
    lunar_phase_tag: str = "day"

    def observe(self) -> Snapshot:
        return Snapshot({"t": self.t, "lunar_phase_tag": self.lunar_phase_tag})

    def step_exogenous(self, dt: float, rng: random.Random) -> None:
        self.t += dt
        # optional: update lunar_phase_tag based on t
