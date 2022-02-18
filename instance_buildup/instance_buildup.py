#!/usr/bin/env python3

import tsp_reader
import sys
from tsp_types import Instance, Tour
import random
import two_opt
import tsp_math

def make_randomized_tour(instance: Instance) -> Tour:
    tour = list(instance.keys())
    random.shuffle(tour)
    return tour

def hill_climb(instance: Instance) -> Tour:
    remaining_points = make_randomized_tour(instance=instance)
    INITIAL_TOUR_SIZE = 4
    tour = remaining_points[-INITIAL_TOUR_SIZE:]
    remaining_points = remaining_points[:-INITIAL_TOUR_SIZE]
    assert(len(instance) == len(remaining_points) + len(tour))
    while remaining_points:
        print(f"current tour len: {len(tour)}")
        tour = two_opt.hill_climb(instance=instance, tour=tour)
        tour = tsp_math.min_cost_insertion(instance=instance, tour=tour, new_point_id=remaining_points.pop())
    assert(len(instance) == len(tour))
    return two_opt.hill_climb(instance=instance, tour=tour)

if __name__ == "__main__":
    instance = tsp_reader.read_instance(sys.argv[1])
    tour = hill_climb(instance=instance)
    tour_length = tsp_math.tour_length(instance=instance, tour=tour)
    print(f"final tour length: {tour_length}")

