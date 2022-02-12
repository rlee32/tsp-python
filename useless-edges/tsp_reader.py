#!/usr/bin/env python3

from typing import Dict, Tuple, List

def read_instance(path: str) -> Dict[int, Tuple[float, float]]:
    """Reads a TSPLIB-formatted TSP instance (not tour) file, and returns it as a dict of point ID to coordinates. """
    instance = {}
    with open(path, "r") as f:
        for line in f:
            if "NODE_COORD_SECTION" in line:
                break
        for line in f:
            line = line.strip()
            if "EOF" in line or not line:
                break
            fields = line.strip().split()
            point_id = int(fields[0])
            x = float(fields[1])
            y = float(fields[2])
            instance[point_id] = (x, y)
    return instance

def read_tour(path: str) -> List[int]:
    """Reads a TSPLIB-formatted TSP tour file, and returns it in the form of an ordered list of point IDs. """
    tour = []
    with open(path, "r") as f:
        for line in f:
            if "TOUR_SECTION" in line:
                break
        for line in f:
            line = line.strip()
            if "-1" in line or "EOF" in line or not line:
                break
            fields = line.strip().split()
            point_id = int(fields[0])
            tour.append(point_id)
    return tour

def distance(instance: Dict[int, Tuple[float, float]], i: int, j: int) -> int:
    """instance is a list of points. each point is a pair of coordinates x, y.
    i and j identify points in the list as indices.
    """
    ix = instance[i][0]
    iy = instance[i][1]
    jx = instance[j][0]
    jy = instance[j][1]
    dx = jx - ix
    dy = jy - iy
    return int(round((dx ** 2 + dy ** 2) ** 0.5))

import sys

if __name__ == "__main__":
    # Test reading an instance and tour.
    if len(sys.argv) > 1:
        instance_path = sys.argv[1]
        print(f"Reading instance file at path: {instance_path}")
        instance = read_instance(path=instance_path)
        print(f"Read {len(instance)} points in instance.")
    if len(sys.argv) > 2:
        tour_path = sys.argv[2]
        print(f"Reading tour file at path: {tour_path}")
        tour = read_tour(path=tour_path)
        print(f"Read {len(tour)} points in tour.")
