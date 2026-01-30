from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class VehicleCommonState:
    vehicle_id: str
    vehicle_type: str              # "mk2", "transporter", "tanker", ...
    role: str                      # "lander", "tug", "tanker", "surface"
    location: str                  # "leo","nrho","lunar_orbit","surface","refurb",...
    phase: str                     # "loiter","transfer","descent","surface","ascent","rendezvous","refurb"
    ready: bool
    health: float                  # 0..1
    flights: int
    assigned_mission: Optional[str] = None

class Vehicle:
    """
    Base interface for vehicles within VehicleFleet.
    """
    def observe(self) -> Dict[str, Any]:
        raise NotImplementedError
