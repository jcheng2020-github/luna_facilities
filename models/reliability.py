from __future__ import annotations
from dataclasses import dataclass
import random
from typing import Tuple

@dataclass
class BetaBernoulli:
    """
    Bernoulli probability model with Beta prior.
    Use this when true failure rates are unknown and should be learned/updated.
    """
    alpha: float = 1.0
    beta: float = 1000.0

    def mean(self) -> float:
        return self.alpha / (self.alpha + self.beta)

    def sample_p(self, rng: random.Random) -> float:
        return rng.betavariate(self.alpha, self.beta)

    def update(self, success: bool) -> None:
        if success:
            self.beta += 1.0
        else:
            self.alpha += 1.0


@dataclass
class EngineFailureModel:
    """
    Two-part failure model:
      - start failure (ignition/transient)
      - in-burn failure per minute (scaled by burn duration)
    """
    start_fail: BetaBernoulli
    burn_fail_per_min: BetaBernoulli

    def draw_outcome(self, burn_minutes: float, health: float, rng: random.Random) -> Tuple[bool, str]:
        """
        Returns (ok, failure_mode). failure_mode: "none" | "start_fail" | "burn_fail"
        """
        # health_factor increases failure probability as health degrades
        health_factor = 1.0 + 2.0 * max(0.0, (1.0 - health))

        p_start = min(1.0, self.start_fail.mean() * health_factor)
        if rng.random() < p_start:
            return False, "start_fail"

        p_min = min(1.0, self.burn_fail_per_min.mean() * health_factor)
        p_burn = 1.0 - (1.0 - p_min) ** max(0.0, burn_minutes)

        if rng.random() < p_burn:
            return False, "burn_fail"

        return True, "none"
