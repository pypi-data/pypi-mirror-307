"""
'Map Projections - A Working Manual' algorithms.
"""
from math import log, tan, pi, atan, exp

from bibliograpy.api import reference

from coordop.bibliography import MAP_PROJECTIONS

@reference(MAP_PROJECTIONS)
def x_7_1(radius: float, cos_phi1: float, lambda0: float, lon: float) -> float:
    """formula 7-1"""
    return radius * (lon - lambda0) * cos_phi1

@reference(MAP_PROJECTIONS)
def y_7_2(radius: float, cos_phi1: float, lat: float) -> float:
    """formula 7-2"""
    return radius * log(tan(pi / 4. + lat / 2.)) * cos_phi1

@reference(MAP_PROJECTIONS)
def phi_7_4(radius: float, cos_phi1: float, y: float) -> float:
    """formula 7-4"""
    return (pi / 2. - 2 * atan(exp(-y / radius))) / cos_phi1

@reference(MAP_PROJECTIONS)
def lambda_7_5(radius: float, cos_phi1: float, lambda0: float, x: float) -> float:
    """formula 7-5"""
    return (x / radius + lambda0) / cos_phi1
