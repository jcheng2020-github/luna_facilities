from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List
import random

from luna_facilities.models.reliability import EngineFailureModel, BetaBernoulli
from luna_facilities.models.cryo import CryoTank
from .base_vehicle import Vehicle, VehicleCommonState


@dataclass
class BE7Engine:
    engine_id: str
    health: float = 1.0
    operable: bool = True
    starts: int = 0
    burn_minutes: float = 0.0

    # Priors are placeholders and should be tuned/learned with real data
    failure_model: EngineFailureModel = field(default_factory=lambda: EngineFailureModel(
        start_fail=BetaBernoulli(1.0, 2000.0),
        burn_fail_per_min=BetaBernoulli(1.0, 20000.0),
    ))

    def attempt_burn(self, minutes: float, rng: random.Random) -> Dict[str, str]:
        if not self.operable:
            return {"status": "fail", "mode": "inoperable"}

        self.starts += 1
        ok, mode = self.failure_model.draw_outcome(minutes, self.health, rng)

        if not ok:
            self.operable = False
            self.health = max(0.0, self.health - 0.2)
            # record failure in priors
            self.failure_model.start_fail.update(False if mode == "start_fail" else True)
            self.failure_model.burn_fail_per_min.update(False if mode == "burn_fail" else True)
            return {"status": "fail", "mode": mode}

        self.burn_minutes += minutes
        self.health = max(0.0, self.health - 0.001 * minutes)  # wear placeholder
        self.failure_model.start_fail.update(True)
        self.failure_model.burn_fail_per_min.update(True)
        return {"status": "ok", "mode": "none"}


@dataclass
class BlueMoonMK2(Vehicle):
    """
    MK2 lander vehicle model.
    - Propellants: LOX/LH2
    - Engines: BE-7 family
    Engine count is configurable due to inconsistent public reporting.
    """
    common: VehicleCommonState

    main_engine_count: int = 3

    lox: CryoTank = field(default_factory=lambda: CryoTank("LOX", 0.0, 200000.0, 0.0005, True))
    lh2: CryoTank = field(default_factory=lambda: CryoTank("LH2", 0.0, 40000.0, 0.0020, True))

    battery_kwh: float = 500.0
    battery_cap_kwh: float = 800.0

    # Certification gates
    completeness_ok: bool = False
    functional_ok: bool = False
    post_refurb_ok: bool = False

    engines: List[BE7Engine] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.engines:
            self.engines = [BE7Engine(f"BE7-{i+1}") for i in range(self.main_engine_count)]

    def observe(self) -> Dict[str, Any]:
        return {
            "common": self.common.__dict__,
            "propellant": {"lox_kg": self.lox.mass_kg, "lh2_kg": self.lh2.mass_kg},
            "battery": {"kwh": self.battery_kwh, "cap_kwh": self.battery_cap_kwh},
            "cert": {
                "completeness_ok": self.completeness_ok,
                "functional_ok": self.functional_ok,
                "post_refurb_ok": self.post_refurb_ok,
            },
            "engines": [{
                "id": e.engine_id,
                "health": e.health,
                "operable": e.operable,
                "starts": e.starts,
                "burn_minutes": e.burn_minutes
            } for e in self.engines]
        }

    def step_cryo(self, days: float) -> Dict[str, float]:
        lost_lox = self.lox.step_boiloff(days)
        lost_lh2 = self.lh2.step_boiloff(days)
        return {"lost_lox": lost_lox, "lost_lh2": lost_lh2}

    def attempt_descent(self, burn_minutes: float, rng: random.Random) -> Dict[str, Any]:
        """
        Simplified: all engines burn during descent.
        """
        events = [e.attempt_burn(burn_minutes, rng) for e in self.engines]
        ok = all(ev["status"] == "ok" for ev in events)

        self.common.phase = "surface" if ok else "abort"
        if ok:
            self.common.flights += 1
        return {"ok": ok, "engine_events": events}
