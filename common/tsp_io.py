#!/usr/bin/env python3

from typing import Dict, Tuple, List
from tsp_types import Tour

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

def write_tour(tour: Tour, path: str):
    with open(path, "w") as f:
        f.write("TOUR_SECTION\n")
        for point in tour:
            f.write(f"{str(point)}\n")
        f.write("-1\n")
        f.write("EOF\n")

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
