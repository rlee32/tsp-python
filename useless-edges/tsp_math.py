#!/usr/bin/env python3

from typing import Dict, Tuple

def distance(instance: Dict[int, Tuple[float, float]], i: int, j: int) -> int:
    """instance is a dict of point IDs to x, y coordinates.
    i and j are the point IDs of the points we want to calculate the distance between.
    Returns distance as rounded int, as per TSPLIB standard.
    """
    ix = instance[i][0]
    iy = instance[i][1]
    jx = instance[j][0]
    jy = instance[j][1]
    dx = jx - ix
    dy = jy - iy
    return int(round((dx ** 2 + dy ** 2) ** 0.5))
