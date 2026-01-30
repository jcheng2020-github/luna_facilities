from __future__ import annotations
from dataclasses import dataclass

@dataclass
class SimConfig:
    dt_hours: float = 1.0
    episode_horizon_steps: int = 24 * 30  # ~30 days at 1-hour dt

    # Hard constraint penalty (treat as termination or huge cost)
    violation_penalty: float = 1e6
