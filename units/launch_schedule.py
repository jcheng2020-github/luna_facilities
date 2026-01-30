from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List
from luna_facilities.core.unit import Unit
from luna_facilities.core.snapshot import Snapshot

@dataclass
class LaunchSchedule(Unit):
    name: str = "LaunchSchedule"
    manifest: List[Dict[str, Any]] = field(default_factory=list)

    def observe(self) -> Snapshot:
        return Snapshot({"manifest": tuple(tuple(sorted(m.items())) for m in self.manifest)})

    def add_launch(self, mission_id: str, planned_time: float, vehicle_id: str, pad_id: str) -> None:
        self.manifest.append({
            "mission_id": mission_id,
            "planned_time": planned_time,
            "vehicle_id": vehicle_id,
            "pad_id": pad_id,
            "status": "planned",
        })

    def set_status(self, mission_id: str, status: str) -> None:
        for m in self.manifest:
            if m["mission_id"] == mission_id:
                m["status"] = status
                return
