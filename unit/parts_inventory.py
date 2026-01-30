from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List
from luna_ops.core.unit import Unit
from luna_ops.core.snapshot import Snapshot

@dataclass
class PartsInventory(Unit):
    name: str = "PartsInventory"
    stock: Dict[str, int] = field(default_factory=dict)
    unit_cost: Dict[str, float] = field(default_factory=dict)
    lead_time_hours: Dict[str, float] = field(default_factory=dict)
    on_order: List[Dict[str, Any]] = field(default_factory=list)

    def observe(self) -> Snapshot:
        return Snapshot({
            "stock": self.stock.copy(),
            "unit_cost": self.unit_cost.copy(),
            "lead_time_hours": self.lead_time_hours.copy(),
            "on_order": tuple(tuple(sorted(x.items())) for x in self.on_order),
        })

    def consume(self, part_id: str, qty: int) -> bool:
        if self.stock.get(part_id, 0) >= qty:
            self.stock[part_id] -= qty
            return True
        return False

    def add_stock(self, part_id: str, qty: int) -> None:
        self.stock[part_id] = self.stock.get(part_id, 0) + max(0, qty)
