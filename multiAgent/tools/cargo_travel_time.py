import math
from typing import Optional
from smolagents import tool

@tool
def cargo_travel_time(
    origin: tuple[float, float],
    destination: tuple[float, float],
    speed: Optional[float] = 750.0,
) -> float:
    """
    Calculate the travel time for a cargo plane between two points on Earth using great-circle distance.

    Args:
        origin: Tuple of (latitude, longitude) for the starting point
        destination: Tuple of (latitude, longitude) for the destination
        speed: Optional cruising speed in km/h (defaults to 750 km/h for typical cargo planes)

    Returns:
        float: The estimated travel time in hours

    Example:
        >>> # Chicago (41.8781° N, 87.6298° W) to Sydney (33.8688° S, 151.2093° E)
        >>> result = calculate_cargo_travel_time((41.8781, -87.6298), (-33.8688, 151.2093))
    """
    
    def to_radians(degrees: float) -> float:
        return degrees * math.pi / 180.0
    
    lat1, lon1 = map(to_radians, origin)
    lat2, lon2 = map(to_radians, destination)

    EARTH_RADIUS_KM = 6371.0
    
    d_lat = lat2 - lat1
    d_lon = lon2 - lon1
    
    a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance_km = EARTH_RADIUS_KM * c
    actual_distance = distance_km * 1.1

    flight_time = (actual_distance / speed) + 1.0
    return flight_time


if __name__ == "__main__":
    print(cargo_travel_time((41.8781, -87.6298), (-33.8688, 151.2093)))