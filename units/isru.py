from __future__ import annotations
from dataclasses import dataclass
import random
from luna_facilities.core.unit import Unit
from luna_facilities.core.snapshot import Snapshot

@dataclass
class ISRUPlant(Unit):
    name: str = "ISRUPlant"

    # outputs per step (kg/step); you can split LOX/LH2
    lox_rate: float = 200.0
    lh2_rate: float = 40.0

    uptime_prob: float = 0.95

    storage_lox: float = 0.0
    storage_lh2: float = 0.0
    storage_cap_lox: float = 1e6
    storage_cap_lh2: float = 2e5

    power_need_kw: float = 200.0

    def observe(self) -> Snapshot:
        return Snapshot(self.__dict__.copy())

    def step_exogenous(self, dt: float, rng: random.Random) -> None:
        if rng.random() < self.uptime_prob:
            self.storage_lox = min(self.storage_cap_lox, self.storage_lox + self.lox_rate)
            self.storage_lh2 = min(self.storage_cap_lh2, self.storage_lh2 + self.lh2_rate)
