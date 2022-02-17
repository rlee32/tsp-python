#!/usr/bin/env python3

from typing import Dict, Tuple, List

Instance = Dict[int, Tuple[float, float]]
Tour = List[int]

def distance(instance: Instance, a: int, b: int) -> int:
    """instance is a dict of point IDs to x, y coordinates.
    a and b are the point IDs of the points we want to calculate the distance between.
    Returns distance as rounded int, as per TSPLIB standard.
    """
    ax = instance[a][0]
    ay = instance[a][1]
    bx = instance[b][0]
    by = instance[b][1]
    dx = bx - ax
    dy = by - ay
    return int(round((dx ** 2 + dy ** 2) ** 0.5))

def tour_length(instance: Instance, tour: Tour) -> int:
    total = 0
    prev = tour[-1]
    for point_id in tour:
        total += distance(instance=instance, a=point_id, b=prev)
        prev = point_id
    return total
