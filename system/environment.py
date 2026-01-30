from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Tuple
import random

from luna_facilities.core.snapshot import Snapshot
from luna_facilities.system.actor_actions import Action
from luna_facilities.system.config import SimConfig
from luna_facilities.system.counter import SystemCounter
from luna_facilities.system.cost import CostModel

@dataclass
class Environment:
    config: SimConfig
    units: Dict[str, Any]                # name -> Unit
    counter: SystemCounter
    cost_model: CostModel = field(default_factory=CostModel)
    rng: random.Random = field(default_factory=lambda: random.Random(0))
    step_count: int = 0

    def observe(self) -> Dict[str, Snapshot]:
        return {name: u.observe() for name, u in self.units.items()}

    def validate_action(self, action: Action) -> Tuple[bool, str]:
        # Central legality checks. Keep it strict later.
        return True, "ok"

    def apply_action(self, action: Action) -> None:
        # Route actions to the correct units
        if action.name == "schedule_launch":
            self.units["LaunchSchedule"].add_launch(
                mission_id=action.params["mission_id"],
                planned_time=float(action.params["planned_time"]),
                vehicle_id=action.params["vehicle_id"],
                pad_id=action.params["pad_id"],
            )

        elif action.name == "command_maneuver":
            self.units["OrbitCatalog"].apply_maneuver(
                asset_id=action.params["asset_id"],
                dv=float(action.params["dv"]),
            )

        elif action.name == "transfer_propellant":
            moved = self.units["PropellantDepot"].transfer(
                depot_id=action.params["depot_id"],
                prop=action.params["prop"],
                amount_kg=float(action.params["amount_kg"]),
            )
            # If you want to actually put propellant into the vehicle:
            fleet = self.units["VehicleFleet"].vehicles
            vid = action.params["vehicle_id"]
            if vid in fleet:
                vobs = fleet[vid].observe()
                # handle MK2 cryo tanks if present
                if "propellant" in vobs:
                    # NOTE: this is a minimalist patch—replace with explicit vehicle APIs if desired.
                    if action.params["prop"] == "LOX":
                        fleet[vid].lox.add(moved)
                    elif action.params["prop"] == "LH2":
                        fleet[vid].lh2.add(moved)

        elif action.name == "start_refurb":
            self.units["RefurbFacility"].start(
                vehicle_id=action.params["vehicle_id"],
                duration_hours=float(action.params["duration_hours"]),
            )

        elif action.name == "run_check":
            # Delegate to inspection unit
            insp = self.units["InspectionAndCheckout"]
            vid = action.params["vehicle_id"]
            ctype = action.params["check_type"]
            if ctype == "completeness":
                insp.run_completeness(vid, self.rng)
            elif ctype == "functional":
                insp.run_functional(vid, self.rng)
            elif ctype == "post_refurb":
                insp.run_post_refurb(vid, self.rng)

    def step(self, action: Action) -> Tuple[Dict[str, Snapshot], float, bool, bool, Dict[str, Any]]:
        dt = self.config.dt_hours

        ok, reason = self.validate_action(action)
        if ok:
            self.apply_action(action)

        # Exogenous evolution
        for u in self.units.values():
            u.step_exogenous(dt, self.rng)

        snaps = self.observe()
        metrics = self.counter.compute_metrics(snaps)
        cost = self.cost_model.total_cost(metrics, self.counter.weights)

        self.step_count += 1
        terminated = metrics.get("violations", 0.0) > 0.0
        truncated = self.step_count >= self.config.episode_horizon_steps

        info = {"metrics": metrics, "action_ok": ok, "action_reason": reason}
        return snaps, cost, terminated, truncated, info
