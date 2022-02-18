#!/usr/bin/env python3

import tsp_reader
import sys
from typing import Optional, Dict, Tuple, List
import tsp_math
import tsp_plot
import random

Edge = Tuple[int, int]
Tour = List[int]
Coordinates = Tuple[float, float]
Instance = Dict[int, Coordinates]

def improve(instance: Instance, tour: Tour) -> Optional[Tour]:
    """If improvement found, new tour is returned. otherwise, None is returned."""
    n = len(tour)
    for i in range(n):
        j_end = n if i > 0 else n - 1
        for j in range(i + 2, j_end):
            a = tour[i]
            b = tour[(i + 1) % n]
            c = tour[j]
            d = tour[(j + 1) % n]
            # current edges
            ab = tsp_math.distance(instance=instance, a=a, b=b)
            cd = tsp_math.distance(instance=instance, a=c, b=d)
            # new edges
            ac = tsp_math.distance(instance=instance, a=a, b=c)
            bd = tsp_math.distance(instance=instance, a=b, b=d)
            if ac + bd < ab + cd:
                return tour[:i+1] + tour[i+1:j+1][::-1] + tour[j+1:]
    return None

def _make_randomized_tour(instance: Instance) -> Tour:
    tour = list(instance.keys())
    random.shuffle(tour)
    return tour

def hill_climb(instance: Instance, tour: Optional[Tour] = None, randomize: bool = False) -> Tour:
    if tour is None:
        tour = list(instance.keys())
    if randomize:
        tour = _make_randomized_tour(instance=instance)
    print(f"Initial tour length: {tsp_math.tour_length(instance=instance, tour=tour)}")
    new_tour = improve(instance=instance, tour=tour)
    iterations = 0
    while new_tour is not None:
        tour = new_tour
        new_tour = improve(instance=instance, tour=tour)
        iterations += 1
    print(f"Done after {iterations} improvements.")
    print(f"Final tour length: {tsp_math.tour_length(instance=instance, tour=tour)}")
    return tour

if __name__ == "__main__":
    instance = tsp_reader.read_instance(sys.argv[1])
    tour = hill_climb(instance=instance, tour=None, randomize=True)
    tsp_plot.plot_tour(instance=instance, tour=tour, show=False)
