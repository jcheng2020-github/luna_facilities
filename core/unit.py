from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List
import random

@dataclass(frozen=True)
class Snapshot:
    data: Dict[str, Any]

class Unit:
    name: str

    def observe(self) -> Snapshot:
        raise NotImplementedError

    def validate(self) -> List[str]:
        return []

    def step_exogenous(self, dt: float, rng: random.Random) -> None:
        """Uncontrolled stochastic evolution."""
        pass
