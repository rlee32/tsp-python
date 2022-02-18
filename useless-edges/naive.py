#!/usr/bin/env python3

# Calculates 'useless edges' using a naive algorithm.
# A 'useless edge' is an edge that is not part of any improving or neutral 2-opt move.

from typing import Optional, Dict, Tuple, List
from tsp_reader import read_instance, read_tour
from tsp_math import distance

Instance = Dict[int, Tuple[float, float]] # point ID to coordinates
Edge = Tuple[int, int] # point ID, point ID

def is_useless_edge(instance: Instance, a: int, b: int) -> bool:
    """Returns True if the input edge specified by 2 endpoint IDs (a, b) is useless. """
    all_indices = list(instance.keys())
    ab = distance(instance=instance, a=a, b=b)
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

def get_non_useless_edges(instance: Instance) -> List[Edge]:
    all_indices = list(instance.keys())
    n = len(all_indices)
    non_useless_edges = []
    useless_edges = []
    for i in range(n):
        print(i)
        a = all_indices[i]
        for j in range(i + 1, n):
            b = all_indices[j]
            if is_useless_edge(instance=instance, a=a, b=b):
                useless_edges.append((a, b))
                continue
            non_useless_edges.append((a, b))
    return non_useless_edges, useless_edges

def get_total_edge_count(instance: Instance) -> int:
    n = len(instance)
    return int(n * (n - 1) / 2)

def get_average_edge_length(instance: Instance, edges: Optional[List[Edge]] = None) -> int:
    length_sum = 0
    if edges:
        for a, b in edges:
            length_sum += distance(instance=instance, a=a, b=b)
        return length_sum / len(edges)
    else:
        all_indices = list(instance.keys())
        n = len(all_indices)
        for i in range(n):
            for j in range(i + 1, n):
                length_sum += distance(instance=instance, a=all_indices[i], b=all_indices[j])
        return length_sum / n

import sys
import mst
from tsp_plot import plot_tour, plot_edge

if __name__ == "__main__":
    # Read instance file.
    if len(sys.argv) > 1:
        instance_path = sys.argv[1]
        print(f"Reading instance file at path: {instance_path}")
        instance = read_instance(path=instance_path)
        print(f"Read {len(instance)} points in instance.")
        total_edge_count = get_total_edge_count(instance=instance)
        print(f"Total edge count: {total_edge_count}")
        print(f"Average edge length {get_average_edge_length(instance)}")
        non_useless_edges, useless_edges = get_non_useless_edges(instance)
        print(f"Non useless edge count: {len(non_useless_edges)}")
        print(f"Non useless edge average length: {get_average_edge_length(instance, non_useless_edges)}")

        # construct length histogram
        non_useless_lengths = {}
        for e in non_useless_edges:
            l = distance(instance=instance, a=e[0], b=e[1])
            if l not in non_useless_lengths:
                non_useless_lengths[l] = 0
            non_useless_lengths[l] += 1
        useless_lengths = {}
        for e in useless_edges:
            l = distance(instance=instance, a=e[0], b=e[1])
            if l not in useless_lengths:
                useless_lengths[l] = 0
            useless_lengths[l] += 1
        for l in non_useless_lengths:
            nue = non_useless_lengths.get(l, 0)
            ue = useless_lengths.get(l, 0)
            print(f"{l}: {nue / (nue + ue)}")

        mst_edges = mst.mst(instance=instance)
        for e in mst_edges:
            if is_useless_edge(instance=instance, a=e[0], b=e[1]):
                print(f"found useless mst edge: {e}")
                # plot useless edges, if optimal tour file supplied.
                if len(sys.argv) > 2:
                    plot_edge(instance=instance, edge=e, linestyle=":", show=False)
            else:
                plot_edge(instance=instance, edge=e, linestyle="b-", show=False)

        # plot optimal tour file.
        if len(sys.argv) > 2:
            tour = read_tour(path=sys.argv[2])
            plot_tour(instance=instance, tour=tour, linestyle='y:')
