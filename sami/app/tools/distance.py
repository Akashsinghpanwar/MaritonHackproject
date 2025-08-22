from __future__ import annotations
from math import radians, sin, cos, asin, sqrt

def distance_nm(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 3440.065  # nautical miles
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    lat1r = radians(lat1)
    lat2r = radians(lat2)
    h = sin(dlat/2)**2 + cos(lat1r)*cos(lat2r)*sin(dlon/2)**2
    return 2*R*asin(sqrt(h))

def eta_days(distance_nm_val: float, speed_knots: float) -> float:
    return distance_nm_val / (24.0 * speed_knots)
