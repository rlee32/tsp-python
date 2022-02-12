#!/usr/bin/env python3

from typing import Dict, Tuple

def distance(instance: Dict[int, Tuple[float, float]], a: int, b: int) -> int:
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
