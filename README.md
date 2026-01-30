
# Luna Facilities RL Simulator (Blue Moon MK2 + Full Campaign System)

This repository is a **modular simulation framework** for developing **ML / RL algorithms** to manage an end-to-end **fully reusable cislunar + lunar transportation system**.

**Blue Moon MK2** is modeled as **one vehicle type** inside a larger campaign-level system that includes:

* launch scheduling and pad conflicts
* orbit state tracking and maneuver management
* comm/range constraints (including blackouts)
* lunar landing site management and traffic control
* orbital/surface propellant depots (including cryo boiloff)
* ISRU production and storage
* surface power allocation
* surface transportation network costs (time/fuel/power)
* refurbishment facility queues and capacity
* inspection and certification gates
* parts inventory and logistics pipeline
* demand model (missions, priorities, deadlines)
* risk model (hard constraints + risk scoring)
* system-wide metrics aggregation and cost function

The core goal is to support **RL-based policies** that can optimize **cadence, reliability, cost, and safety** under uncertainty.

---

## 1) Key Concepts

### Units

A **Unit** is a subsystem that owns part of the world state.
Every unit implements the same interface:

* `observe()` → returns a read-only `Snapshot`
* `step_exogenous(dt, rng)` → stochastic/uncontrolled evolution
* `validate()` → optional state validation checks

Examples: `LaunchSchedule`, `OrbitCatalog`, `ISRUPlant`, `PropellantDepot`, `RefurbFacility`.

### Vehicles

Vehicles live inside a single unit: **VehicleFleet**.
Vehicles are heterogeneous types such as:

* `BlueMoonMK2` (lander; LOX/LH2 cryo tanks; BE-7 engine model)
* `CislunarTransporter` (tug/tanker-like element)

### System

The system layer provides:

* `ActorActions`: standardized action objects for RL policies
* `SystemCounter`: read-only KPI/metric aggregation from unit snapshots
* `CostModel`: converts metrics into scalar cost
* `Environment`: ties everything together and executes transitions

---

## 2) Repository Layout

```
luna_facilities/
  __init__.py

  core/          # base interfaces + shared types
  models/        # reusable physics/probability models (reliability, cryo, parts)
  vehicles/      # vehicle types (MK2, transporter, etc.)
  units/         # system units (orbit, depot, ISRU, refurb, etc.)
  system/        # environment, actions, counter, cost, config
```

### `core/`

* `unit.py`: Base Unit interface
* `snapshot.py`: Read-only observation container
* `types.py`: Typed aliases (VehicleID, MissionID, etc.)

### `models/`

* `reliability.py`: Bayesian failure models (`BetaBernoulli`, `EngineFailureModel`)
* `cryo.py`: cryo tank boiloff model (`CryoTank`)
* `parts_catalog.py`: generic parts catalog + replacement policy

### `vehicles/`

* `base_vehicle.py`: `Vehicle` and `VehicleCommonState`
* `blue_moon_mk2.py`: MK2 lander model (engines + cryo + cert gates)
* `cislunar_transporter.py`: generic transporter/tug model

### `units/`

Includes all major subsystems (launch, orbit, comms, depot, ISRU, refurb, inspection, inventory, logistics, demand, risk, etc.) plus:

* `vehicle_fleet.py`: container for all vehicles (including MK2)

### `system/`

* `actor_actions.py`: action definitions for RL policies
* `counter.py`: KPI aggregation
* `cost.py`: scalar cost function
* `environment.py`: step loop + action routing
* `config.py`: sim configuration (dt, horizon, penalties)

---

## 3) How the Simulation Works

Each environment step follows this pattern:

1. **Policy chooses an action** `Action(name, params)`
2. `Environment.validate_action(action)` checks legality (placeholder currently)
3. `Environment.apply_action(action)` routes to the correct unit(s)
4. All units run `step_exogenous(dt)` for stochastic evolution
5. `SystemCounter.compute_metrics(snapshots)` produces KPIs
6. `CostModel.total_cost(metrics, weights)` returns scalar cost
7. Returns `(obs, cost, terminated, truncated, info)` (Gymnasium-style)

---

## 4) Quick Start (Minimal Example)

### Requirements

* Python 3.10+ recommended

Install dependencies (example):

```bash
pip install -U numpy
```

### Minimal bootstrap snippet

Create a script such as `bootstrap_demo.py`:

```python
from luna_facilities.system.config import SimConfig
from luna_facilities.system.environment import Environment
from luna_facilities.system.counter import SystemCounter
from luna_facilities.system.actor_actions import ActorActions

from luna_facilities.units.launch_schedule import LaunchSchedule
from luna_facilities.units.orbit_catalog import OrbitCatalog
from luna_facilities.units.propellant_depot import PropellantDepot
from luna_facilities.units.refurb_facility import RefurbFacility
from luna_facilities.units.inspection import InspectionAndCheckout
from luna_facilities.units.vehicle_fleet import VehicleFleet

from luna_facilities.vehicles.blue_moon_mk2 import BlueMoonMK2
from luna_facilities.vehicles.base_vehicle import VehicleCommonState

# Build units
units = {
    "LaunchSchedule": LaunchSchedule(),
    "OrbitCatalog": OrbitCatalog(),
    "PropellantDepot": PropellantDepot(),
    "RefurbFacility": RefurbFacility(),
    "InspectionAndCheckout": InspectionAndCheckout(),
    "VehicleFleet": VehicleFleet(),
}

# Add a MK2 lander into the fleet
mk2 = BlueMoonMK2(
    common=VehicleCommonState(
        vehicle_id="MK2-01",
        vehicle_type="mk2",
        role="lander",
        location="nrho",
        phase="loiter",
        ready=True,
        health=1.0,
        flights=0,
    ),
    main_engine_count=3,
)

units["VehicleFleet"].vehicles["MK2-01"] = mk2

# Create environment
cfg = SimConfig(dt_hours=1.0, episode_horizon_steps=24)
counter = SystemCounter()

env = Environment(config=cfg, units=units, counter=counter)

# Step the environment with an example action
action = ActorActions.start_refurb(vehicle_id="MK2-01", duration_hours=12.0)
obs, cost, terminated, truncated, info = env.step(action)

print("cost:", cost)
print("terminated:", terminated, "truncated:", truncated)
print("metrics:", info["metrics"])
```

Run:

```bash
python bootstrap_demo.py
```

---

## 5) Extending the Model

### Add new vehicle types

1. Create a class in `vehicles/` that implements:

   * `observe() -> Dict[str, Any]`
2. Add instances into `VehicleFleet.vehicles`

### Add new subsystems (units)

1. Create a class in `units/` extending `Unit`
2. Register it in `Environment.units`
3. Update action routing in `Environment.apply_action()`
4. Add KPI extraction in `SystemCounter.compute_metrics()`

---

## 6) RL Integration Guidance

This simulator is designed so you can wrap it as a Gymnasium environment.

Recommended next steps:

* Define a stable observation representation:

  * dict observations for prototype
  * vectorized observations for training
* Define action space:

  * discrete (high-level choices) or
  * parameterized actions (`Action(name, params)`)
* Add legality checks + masking (important for RL stability)
* Separate **hard constraints** (terminate episode) vs **soft penalties** (large cost)

---

## 7) Configuration and Uncertainty

Some parameters are **not publicly known** (e.g., true engine failure rates, MK2 maintenance BOM).
This repo handles that by:

* using **Bayesian priors** for failures (`BetaBernoulli`)
* using **replace-policy models** for parts (every-turn / every-N / on-condition)
* keeping major assumptions **explicit and configurable**

---

## 8) Roadmap Suggestions

High-value upgrades:

1. Implement `Environment.validate_action()` with real constraints (pads, comm blackouts, propellant reserves, cert gates)
2. Add vehicle APIs for propellant transfer and power draw (avoid direct attribute edits)
3. Build `SystemCounter` metrics:

   * schedule lateness
   * delivered payload
   * propellant and energy consumption
   * fleet readiness and turnaround time
   * constraint violations
4. Add a `bootstrap.py` that instantiates the full system with reasonable defaults
5. Provide a Gymnasium wrapper for Stable-Baselines3 or RLlib

---

## 9) License / Usage

Internal research / prototype use.
If you plan to open-source, add:

* LICENSE file
* CITATION file (optional)
* CONTRIBUTING guidelines

