#!/usr/bin/env python3

# Kruskal's algorithm. Aiming for implementation simplicity, rather than efficiency.

from typing import Optional, Dict, Tuple, List

from tsp_reader import read_instance
from tsp_math import distance
import random

Instance = Dict[int, Tuple[float, float]] # point ID to coordinates
Edge = Tuple[int, int, int] # distance, min point ID, max point ID

def make_edge(instance: Instance, a: int, b: int) -> Edge:
    n = len(instance)
    return (distance(instance=instance, a=a, b=b), min(a, b), max(a, b))

def make_sorted_edges(instance: Instance) -> List[Edge]:
    """ returns all possible edges sorted by cost. complexity is at least O(n**2 * log(n**2))
    """
    edges = []
    n = len(instance)
    all_ids = list(instance.keys())
    for i in range(n):
        a = all_ids[i]
        for j in range(i + 1, n):
            b = all_ids[j]
            randint = random.randint(0, n)
            # add a random int so that edges arent deterministically placed in the MST.
            edge = make_edge(instance, a=a, b=b)
            edge = (edge[0], randint, edge[1], edge[2])
            edges.append(edge)
    edges.sort()
    # take out the random int.
    edges = [(edge[0], edge[2], edge[3]) for edge in edges]
    return edges

def mst(instance: Instance) -> List[Edge]:
    """Returns MST for given instance.
    """
    sorted_edges = make_sorted_edges(instance)
    sets = []
    edges = []
    for e in sorted_edges:
        # determine which edge sets this new edge belongs to.
        found = []
        cyclic = False
        a = e[1]
        b = e[2]
        for i in range(len(sets)):
            if a in sets[i] and b in sets[i]:
                cyclic = True
                break
            elif a in sets[i] or b in sets[i]:
                found.append(i)
        if cyclic:
            continue
        assert(len(found) <= 2)

        # create new set, add to existing, or merge 2 existing.
        if len(found) == 0:
            sets.append(set())
            sets[-1].add(a)
            sets[-1].add(b)
        elif len(found) == 1:
            sets[found[0]].add(a)
            sets[found[0]].add(b)
        elif len(found) == 2:
            sets[found[0]].update(sets[found[1]])
            sets.pop(found[1])
        edges.append(e)

        # end if all points included.
        if len(edges) == len(instance):
            break

    # check that result touches all points.
    check = set()
    for e in edges:
        a = e[1]
        check.add(a)
        b = e[2]
        check.add(b)
    assert(len(check) == len(instance))

    return edges

def get_degree_to_points(edges: List[Edge]):
    point_to_degree = {}
    for edge in edges:
        for point_id in edge:
            point_to_degree[point_id] = point_to_degree.get(point_id, 0) + 1
    degree_to_points = {}
    for point_id in point_to_degree:
        deg = point_to_degree[point_id]
        if deg not in degree_to_points:
            degree_to_points[deg] = []
        degree_to_points[deg].append(point_id)
    return degree_to_points

import sys
import tsp_plot

if __name__ == "__main__":
    instance_file = sys.argv[1]
    instance = read_instance(instance_file)
    edges = mst(instance=instance)
    total = sum([e[0] for e in edges])
    print(f'total cost: {total}')

    degree_to_points = get_degree_to_points(edges = edges)
    high_deg_points = []
    for deg in degree_to_points:
        if deg >= 3:
            high_deg_points += degree_to_points[deg]

    edges = [edge[1:] for edge in edges]
    tsp_plot.plot_edges(instance=instance, edges=edges, show=False)
    tsp_plot.plot_points_by_ids(instance=instance, point_ids=high_deg_points, style='ro', show=True)
