#!/usr/bin/env python3

import tsp_reader
import mst
import two_opt
import sys
from typing import List
from tsp_types import Edge, Tour, Instance
import tsp_math

def normalize_edge(edge: Edge) -> Edge:
    a, b = edge
    return (min(a, b), max(a, b))

def normalize_edges(edges: List[Edge]) -> List[Edge]:
    return [normalize_edge(edge) for edge in edges]

def get_new_edges(tour: Tour, edges: List[Edge]) -> List[Edge]:
    edges = normalize_edges(edges=edges)
    tour_edges = tsp_math.get_edges_from_tour(tour=tour)
    tour_edges = set(normalize_edges(edges=tour_edges))
    new_edges = []
    for edge in edges:
        if edge not in tour_edges:
            new_edges.append(edge)
    return new_edges

def hill_climb(original_instance: Instance, tour: Tour) -> Tour:
    instance = original_instance.copy()
    original_tour = tour[:]
    initial_tour_length = tsp_math.tour_length(instance=instance, tour=tour)
    mst_edges = mst.mst(instance=instance)
    new_edges = get_new_edges(tour=tour, edges=mst_edges)
    print(f"adding {len(new_edges)} new mst edges.")
    new_point_ids = tsp_math.add_midpoints_to_instance(instance=instance, edges=new_edges)
    print(f"new instance size: {len(instance)}")
    tour_set = set(tour)
    for point_id in instance:
        if point_id in tour_set:
            continue
        tour = tsp_math.min_cost_insertion(instance=instance, tour=tour, new_point_id=point_id)
    tour = two_opt.hill_climb(instance=instance, tour=tour)
    augmented_size = len(tour)
    print(f"augmented tour length: {tsp_math.tour_length(instance=instance, tour=tour)}")
    for p in new_point_ids:
        tour.remove(p)
    print(f"reduced tour length: {tsp_math.tour_length(instance=instance, tour=tour)}")
    tour = two_opt.hill_climb(instance=instance, tour=tour)
    final_local_optimum = tsp_math.tour_length(instance=instance, tour=tour)
    print(f"final tour length: {final_local_optimum}")
    assert(len(tour) + len(new_point_ids) == augmented_size)
    print(f"scaffolding: {initial_tour_length} -> {final_local_optimum}")
    print()
    if initial_tour_length < final_local_optimum:
        return original_tour
    else:
        return tour

if __name__ == "__main__":
    instance_file = sys.argv[1]
    instance = tsp_reader.read_instance(instance_file)
    tour = two_opt.hill_climb(instance=instance, tour=None, randomize=True)

    while True:
        tour = hill_climb(original_instance=instance, tour=tour)
