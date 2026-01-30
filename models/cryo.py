from __future__ import annotations
from dataclasses import dataclass

@dataclass
class CryoTank:
    """
    Simple cryogenic tank model with optional "zero boiloff" mode.
    Fractions are per-day; convert dt to days at the call site.
    """
    prop_name: str
    mass_kg: float
    capacity_kg: float
    boiloff_frac_per_day: float
    zero_boiloff_enabled: bool = True

    def add(self, amount_kg: float) -> float:
        accepted = min(amount_kg, self.capacity_kg - self.mass_kg)
        self.mass_kg += max(0.0, accepted)
        return max(0.0, accepted)

    def remove(self, amount_kg: float) -> float:
        taken = min(self.mass_kg, max(0.0, amount_kg))
        self.mass_kg -= taken
        return taken

    def step_boiloff(self, days: float) -> float:
        if self.zero_boiloff_enabled:
            return 0.0
        before = self.mass_kg
        self.mass_kg = max(0.0, self.mass_kg * (1.0 - self.boiloff_frac_per_day) ** max(0.0, days))
        return before - self.mass_kg
