from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple

@dataclass
class Event:
    start: datetime
    end: datetime
    reason: str
    excepted: bool  # True if time does NOT count toward laytime

@dataclass
class CP:
    laytime_hours: float = 72.0
    shex_eiu: bool = True
    demurrage_per_day: float = 15000.0
    despatch_per_day: float = 7500.0
    shore_breakdown_counts: bool = True

def compute_laytime(cp: CP, counting_periods: List[Event]) -> Tuple[float, float, float]:
    """Return: (used_hours, demurrage_usd, despatch_usd)"""
    used_seconds = 0.0
    for e in counting_periods:
        if e.excepted:
            continue
        used_seconds += (e.end - e.start).total_seconds()
    used_hours = used_seconds / 3600.0

    diff_hours = used_hours - cp.laytime_hours
    if diff_hours > 0:
        demurrage = (diff_hours / 24.0) * cp.demurrage_per_day
        return used_hours, round(demurrage, 2), 0.0
    elif diff_hours < 0:
        despatch = (-diff_hours / 24.0) * cp.despatch_per_day
        return used_hours, 0.0, round(despatch, 2)
    return used_hours, 0.0, 0.0
