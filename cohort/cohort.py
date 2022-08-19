#!/usr/bin/env python3

import tsp_reader
import twoopt
import sys
from typing import Optional, Dict, Tuple, List
import tsp_math
import tsp_plot
import mst
import random

Edge = Tuple[int, int]
Tour = List[int]
Coordinates = Tuple[float, float]
Instance = Dict[int, Coordinates]

def make_randomized_tour(instance: Instance) -> Tour:
    tour = list(instance.keys())
    random.shuffle(tour)
    return tour

def remove_dupes(instance: Instance, tours: List[Tour]):
    return_tours = []
    for i in range(len(tours)):
        duped = False
        for j in range(i + 1, len(tours)):
            if tsp_math.is_dupe(instance=instance, tour=tours[i], other_tour=tours[j]):
                duped = True
                break
        if not duped:
            return_tours.append(tours[i])
    return return_tours

def is_dupe(instance: Instance, tours: List[Tour], tour: Tour):
    for other in tours:
        if tsp_math.is_dupe(instance=instance, tour=tour, other_tour=other):
            return True
    return False

def clique_combine(instance: Instance, bests: List[Tour], n: int):
    n_bests = len(bests)
    for i in range(n_bests):
        for j in range(i + 1, n_bests):
            maybe_new_tour = tsp_math.integrate_tour(instance=instance, best_tour=bests[i], new_tour=bests[j])
            if maybe_new_tour and not is_dupe(instance=instance, tours=bests, tour=maybe_new_tour):
                bests.append(maybe_new_tour)
    bests = sorted(bests, key = lambda x: tsp_math.tour_length(instance=instance, tour=x))[:n]
    bests = remove_dupes(instance=instance, tours=bests)
    print(f"clique_combine bests length: {len(bests)}")
    best_cost = tsp_math.tour_length(instance=instance, tour=bests[0])
    print(f"clique_combine best cost: {best_cost}")
    return bests

def try_new_tour(instance: Instance, bests: List[Tour], n: int):
    new_tour = twoopt.hill_climb(instance=instance, tour=make_randomized_tour(instance=instance))
    for best in bests:
        maybe_new_tour = tsp_math.integrate_tour(instance=instance, best_tour=best, new_tour=new_tour)
        if maybe_new_tour and not is_dupe(instance=instance, tours=bests, tour=maybe_new_tour):
            bests.append(maybe_new_tour)
    bests.append(new_tour)
    bests = sorted(bests, key = lambda x: tsp_math.tour_length(instance=instance, tour=x))
    bests = remove_dupes(instance=instance, tours=bests)
    print(f"try_new_tour bests length: {len(bests)}")
    best_cost = tsp_math.tour_length(instance=instance, tour=bests[0])
    print(f"try_new_tour best cost: {best_cost}")
    return clique_combine(instance=instance, bests=bests, n=n)

def climb(instance: Instance, n: int):
    """Perform tour-differencing optimization, keeping the n best tours to compare among. """
    bests = []
    while True:
        bests = try_new_tour(instance=instance, bests=bests, n=n)

if __name__ == "__main__":
    instance = tsp_reader.read_instance(sys.argv[1])
    climb(instance=instance, n = 50)

    # Visualization
    """
    tsp_plot.plot_tour(instance=instance, tour=tour, show=False)

    edges = mst.mst(instance=instance)
    tsp_plot.plot_edges(instance=instance, edges=edges, linestyle="g-.", show=False)

    opt_tour = tsp_reader.read_tour(sys.argv[2])
    tsp_plot.plot_tour(instance=instance, tour=opt_tour, linestyle="b:")
    """
