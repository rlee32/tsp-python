#!/usr/bin/env python3

# Kruskal's algorithm. Aiming for implementation simplicity, rather than efficiency.

from typing import Optional, Dict, Tuple, List

from tsp_reader import read_instance
from tsp_math import distance

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
            edges.append(make_edge(instance, a=a, b=b))
    edges.sort()
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

import sys

if __name__ == "__main__":
    instance_file = sys.argv[1]
    instance = read_instance(instance_file)
    edges = mst(instance=instance)
    total = sum([e[0] for e in edges])
    print(f'total cost: {total}')

    #plot_edges(instance, edges)
    #plot_tour(instance, tour)
    #plot_diff(instance, tour, edges)
    #plt.axis('square')
    #plt.show()
