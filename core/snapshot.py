from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict

@dataclass(frozen=True)
class Snapshot:
    """
    Read-only observation payload returned by Units.
    Must be serializable / stable enough for logging.
    """
    data: Dict[str, Any]
