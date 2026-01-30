from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class PartSpec:
    part_id: str
    description: str
    unit_cost: float
    replace_policy: str  # "every_turn" | "every_n_cycles" | "on_condition"
    n_cycles: int = 0

def default_part_catalog() -> Dict[str, PartSpec]:
    """
    Program-level generic catalog. You can specialize per vehicle type if desired.
    NOTE: These are modeling placeholders (not MK2 BOM facts).
    """
    return {
        "seal_kit": PartSpec("seal_kit", "Cryo valve seals/O-rings kit", 500.0, "every_turn"),
        "filter_set": PartSpec("filter_set", "Propellant filters set", 1200.0, "every_turn"),
        "qd_seal_set": PartSpec("qd_seal_set", "Quick-disconnect seal set", 900.0, "every_turn"),

        "sensor_unit": PartSpec("sensor_unit", "Flight sensor unit", 5000.0, "on_condition"),
        "avionics_box": PartSpec("avionics_box", "Avionics box replaceable unit", 25000.0, "on_condition"),

        "valve_actuator": PartSpec("valve_actuator", "Valve actuator assembly", 25000.0, "every_n_cycles", n_cycles=20),
        "turbo_bearing": PartSpec("turbo_bearing", "Turbomachinery bearing kit", 80000.0, "every_n_cycles", n_cycles=50),
        "mli_panel": PartSpec("mli_panel", "Thermal blanket / MLI panel", 15000.0, "every_n_cycles", n_cycles=30),
        "landing_damper": PartSpec("landing_damper", "Landing damper/crush core", 40000.0, "every_n_cycles", n_cycles=10),
    }
