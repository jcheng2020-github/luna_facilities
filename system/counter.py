from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict
from luna_ops.core.unit import Unit
from luna_ops.core.snapshot import Snapshot

@dataclass
class SystemCounter(Unit):
    """
    Read-only aggregator: computes metrics and exposes them to CostModel.
    """
    name: str = "SystemCounter"
    weights: Dict[str, float] = field(default_factory=lambda: {
        "lateness": 1.0,
        "propellant_used": 1.0,
        "energy_used": 1.0,
        "refurb_hours": 0.2,
        "risk": 10.0,
        "violations": 1e6,
    })

    def observe(self) -> Snapshot:
        return Snapshot({"weights": self.weights})

    def compute_metrics(self, snaps: Dict[str, Snapshot]) -> Dict[str, float]:
        # Keep this deterministic and read-only
        m = {
            "lateness": 0.0,
            "propellant_used": 0.0,
            "energy_used": 0.0,
            "refurb_hours": 0.0,
            "risk": 0.0,
            "violations": 0.0,
        }

        # Example: refurb queue pressure as a proxy
        refurb = snaps.get("RefurbFacility")
        if refurb:
            in_service = refurb.data.get("in_service", {})
            m["refurb_hours"] = float(sum(max(0.0, v) for v in in_service.values()))

        return m
