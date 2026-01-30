from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict
import random
from luna_facilities.core.unit import Unit
from luna_facilities.core.snapshot import Snapshot

@dataclass
class InspectionAndCheckout(Unit):
    name: str = "InspectionAndCheckout"

    completeness: Dict[str, bool] = field(default_factory=dict)
    functional: Dict[str, bool] = field(default_factory=dict)
    post_refurb: Dict[str, bool] = field(default_factory=dict)

    def observe(self) -> Snapshot:
        return Snapshot({
            "completeness": self.completeness.copy(),
            "functional": self.functional.copy(),
            "post_refurb": self.post_refurb.copy(),
        })

    def run_completeness(self, vehicle_id: str, rng: random.Random) -> bool:
        ok = rng.random() > 0.02
        self.completeness[vehicle_id] = ok
        return ok

    def run_functional(self, vehicle_id: str, rng: random.Random) -> bool:
        ok = rng.random() > 0.03
        self.functional[vehicle_id] = ok
        return ok

    def run_post_refurb(self, vehicle_id: str, rng: random.Random) -> bool:
        ok = rng.random() > 0.01
        self.post_refurb[vehicle_id] = ok
        return ok
