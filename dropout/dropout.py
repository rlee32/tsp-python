#!/usr/bin/env python3

import tsp_reader
import two_opt
import sys
from typing import List
from tsp_types import Edge, Tour, Tuple, Instance
import tsp_math
import random

THRESHOLD = 35
MAX_INT = 100

def random_drop(threshold: int, max_int: int) -> bool:
    assert(threshold < max_int)
    return random.randint(0, max_int) < threshold

def drop_points(tour: Tour, threshold: int, max_int: int) -> Tuple[Tour, List[int]]:
    new_tour = []
    dropped = []
    for p in tour:
        if random_drop(threshold=threshold, max_int=max_int):
            dropped.append(p)
        else:
            new_tour.append(p)
    print(f"dropped {round(len(dropped) / len(tour) * 100)} %")
    return new_tour, dropped

def hill_climb(instance: Instance, tour: Tour) -> Tour:
    new_tour, dropped = drop_points(tour=tour, threshold=THRESHOLD, max_int=MAX_INT)
    new_tour = two_opt.hill_climb(instance=instance, tour=new_tour)
    for p in dropped:
        new_tour = tsp_math.min_cost_insertion(instance=instance, tour=new_tour, new_point_id=p)
    new_tour = two_opt.hill_climb(instance=instance, tour=new_tour)
    new_length = tsp_math.tour_length(instance=instance, tour=new_tour)
    original_length = tsp_math.tour_length(instance=instance, tour=tour)
    print(f"dropout: {original_length} -> {new_length}")
    kmoves = tsp_math.get_kmoves_between_tours(old_tour=tour, new_tour=new_tour)
    print(f"got {len(kmoves)} kmoves.")
    print()
    if new_length < original_length:
        return new_tour
    else:
        return tour


if __name__ == "__main__":
    instance_file = sys.argv[1]
    instance = tsp_reader.read_instance(instance_file)
    tour = two_opt.hill_climb(instance=instance, tour=None, randomize=True)

    iteration = 0
    while True:
        tour = hill_climb(instance=instance, tour=tour)
        iteration += 1
        print(f"iteration: {iteration}")
