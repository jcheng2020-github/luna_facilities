from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any

from .base_vehicle import Vehicle, VehicleCommonState

@dataclass
class CislunarTransporter(Vehicle):
    """
    Generic tug/transporter (architecture element).
    This can represent tankers/tugs moving cargo/propellant between orbits.
    """
    common: VehicleCommonState

    propellant_kg: float = 0.0
    propellant_cap_kg: float = 150000.0

    dv_budget_mps: float = 2000.0
    dv_remaining_mps: float = 2000.0

    def observe(self) -> Dict[str, Any]:
        return {
            "common": self.common.__dict__,
            "propellant_kg": self.propellant_kg,
            "propellant_cap_kg": self.propellant_cap_kg,
            "dv_remaining_mps": self.dv_remaining_mps,
        }
