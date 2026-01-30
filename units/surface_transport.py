from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Tuple
from luna_facilities.core.unit import Unit
from luna_facilities.core.snapshot import Snapshot

@dataclass
class SurfaceTransportNetwork(Unit):
    name: str = "SurfaceTransportNetwork"
    edges: Dict[Tuple[str, str], Dict[str, float]] = field(default_factory=dict)  # (src,dst)->{time,fuel,power}
    vehicles_available: int = 10

    def observe(self) -> Snapshot:
        return Snapshot({"edges": self.edges, "vehicles_available": self.vehicles_available})

    def route_cost(self, src: str, dst: str) -> Dict[str, float]:
        return self.edges.get((src, dst), {"time": float("inf"), "fuel": float("inf"), "power": float("inf")})
