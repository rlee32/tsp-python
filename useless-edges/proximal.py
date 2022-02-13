#!/usr/bin/env python3

# Calculates 'useless edges' using a naively-implemented, but theoretically efficient algorithm.
# A 'useless edge' is an edge that is not a part of any improving 2-opt move.

from typing import Dict, Tuple, List
from tsp_reader import read_instance
from tsp_math import distance

def get_nearby_points(instance: Dict[int, Tuple[float, float]], center: int, radius: int) -> List[int]:
    nearby_points = []
    for p in instance:
        if p == center:
            continue
        if distance(instance=instance, a=center, b=p) <= radius:
            nearby_points.append(p)
    return nearby_points

def is_useless_edge(instance: Dict[int, Tuple[float, float]], a: int, b: int) -> bool:
    """Returns True if the input edge specified by 2 endpoint IDs (a, b) is useless. """
    all_indices = list(instance.keys())
    ab = distance(instance=instance, a=a, b=b)
    a_nearby = get_nearby_points(instance=instance, center=a, radius=ab)
    for c in a_nearby:
        if c == b:
            continue
        ac = distance(instance=instance, a=a, b=c)
        c_nearby = get_nearby_points(instance=instance, center=c, radius=ab - ac)
        for e in c_nearby:
            ce = distance(instance=instance, a=c, b=e)


    # TODO: under construction!


    for c in all_indices:
        if c in (a, b):
            continue
        c_useless = True
        for d in all_indices:
            if d in (a, b, c):
                continue
            cd = distance(instance=instance, a=c, b=d)
            ac = distance(instance=instance, a=a, b=c)
            bd = distance(instance=instance, a=b, b=d)
            if ab + cd < ac + bd:
                c_useless = False
                break
            ad = distance(instance=instance, a=a, b=d)
            bc = distance(instance=instance, a=b, b=c)
            if ab + cd < ad + bc:
                c_useless = False
                break
        if c_useless:
            return True
    return False

def get_non_useless_edges(instance: Dict[int, Tuple[float, float]]) -> List[Tuple[int, int]]:
    all_indices = list(instance.keys())
    n = len(all_indices)
    non_useless_edges = []
    for i in range(n):
        print(i)
        a = all_indices[i]
        for j in range(i + 1, n):
            b = all_indices[j]
            if is_useless_edge(instance=instance, a=a, b=b):
                continue
            non_useless_edges.append((a, b))
    return non_useless_edges

def get_total_edge_count(instance: Dict[int, Tuple[float, float]]) -> int:
    n = len(instance)
    return int(n * (n - 1) / 2)

import sys

if __name__ == "__main__":
    # Read instance file.
    if len(sys.argv) > 1:
        instance_path = sys.argv[1]
        print(f"Reading instance file at path: {instance_path}")
        instance = read_instance(path=instance_path)
        print(f"Read {len(instance)} points in instance.")
        total_edge_count = get_total_edge_count(instance=instance)
        print(f"Total edge count: {total_edge_count}")
        non_useless_edges = get_non_useless_edges(instance)
        print(f"Non useless edge count: {len(non_useless_edges)}")

