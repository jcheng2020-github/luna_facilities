from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict

@dataclass(frozen=True)
class Action:
    name: str
    params: Dict[str, Any]

class ActorActions:
    # Scheduling
    @staticmethod
    def schedule_launch(mission_id: str, planned_time: float, vehicle_id: str, pad_id: str) -> Action:
        return Action("schedule_launch", {"mission_id": mission_id, "planned_time": planned_time, "vehicle_id": vehicle_id, "pad_id": pad_id})

    # Orbit
    @staticmethod
    def command_maneuver(asset_id: str, dv: float, purpose: str = "generic") -> Action:
        return Action("command_maneuver", {"asset_id": asset_id, "dv": dv, "purpose": purpose})

    # Propellant logistics
    @staticmethod
    def transfer_propellant(depot_id: str, prop: str, vehicle_id: str, amount_kg: float) -> Action:
        return Action("transfer_propellant", {"depot_id": depot_id, "prop": prop, "vehicle_id": vehicle_id, "amount_kg": amount_kg})

    # Refurb & checks
    @staticmethod
    def start_refurb(vehicle_id: str, duration_hours: float) -> Action:
        return Action("start_refurb", {"vehicle_id": vehicle_id, "duration_hours": duration_hours})

    @staticmethod
    def run_check(vehicle_id: str, check_type: str) -> Action:
        return Action("run_check", {"vehicle_id": vehicle_id, "check_type": check_type})
