from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict
from luna_ops.core.unit import Unit
from luna_ops.core.snapshot import Snapshot

@dataclass
class LandingSiteManager(Unit):
    name: str = "LandingSiteManager"
    pads: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    def observe(self) -> Snapshot:
        return Snapshot({"pads": self.pads})

    def reserve_pad(self, pad_id: str, vehicle_id: str, t0: float, t1: float) -> None:
        self.pads.setdefault(pad_id, {})
        self.pads[pad_id]["reservation"] = {"vehicle_id": vehicle_id, "t0": t0, "t1": t1}
