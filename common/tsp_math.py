#!/usr/bin/env python3

from typing import Tuple, List
from tsp_types import Instance, Tour, Edge
import math

def distance(instance: Instance, a: int, b: int) -> int:
    """instance is a dict of point IDs to x, y coordinates.
    a and b are the point IDs of the points we want to calculate the distance between.
    Returns distance as rounded int, as per TSPLIB standard.
    """
    ax = instance[a][0]
    ay = instance[a][1]
    bx = instance[b][0]
    by = instance[b][1]
    dx = bx - ax
    dy = by - ay
    return int(round((dx ** 2 + dy ** 2) ** 0.5))

def tour_length(instance: Instance, tour: Tour) -> int:
    total = 0
    prev = tour[-1]
    for point_id in tour:
        total += distance(instance=instance, a=point_id, b=prev)
        prev = point_id
    return total

def get_edges_from_tour(tour: Tour) -> Tuple[Edge]:
    edges = []
    prev = tour[-1]
    for point_id in tour:
        edges.append((prev, point_id))
        prev = point_id
    return edges

def min_cost_insertion(instance: Instance, tour: Tour, new_point_id: int) -> Tour:
    edges = get_edges_from_tour(tour=tour)
    p = new_point_id
    min_cost = math.inf
    min_replacement = None
    for edge in edges:
        a, b = edge
        ab = distance(instance=instance, a=a, b=b)
        pa = distance(instance=instance, a=p, b=a)
        pb = distance(instance=instance, a=p, b=b)
        diff = pa + pb - ab
        if diff == min_cost:
            min_replacement.append(edge)
        elif diff < min_cost:
            min_cost = diff
            min_replacement = [edge]
    old_edge = min_replacement[0] # TODO: have multiple methods for choosing among candidates.
    a, b = old_edge
    i = tour.index(a)
    j = tour.index(b)
    diff = abs(i - j)
    if diff == 1:
        return tour[:max(i, j)] + [p] + tour[max(i, j):]
    else:
        assert(min(i, j) == 0)
        return tour + [p]

def add_midpoint_to_instance(instance: Instance, edge: Edge):
    a, b = edge
    ax = instance[a][0]
    ay = instance[a][1]
    bx = instance[b][0]
    by = instance[b][1]
    dx = bx - ax
    dy = by - ay
    new_id = max(instance.keys()) + 1
    instance[new_id] = (ax + dx / 2, ay + dy / 2)
    return new_id

def add_midpoints_to_instance(instance: Instance, edges: List[Edge]):
    new_point_ids = []
    for edge in edges:
        new_point_ids.append(add_midpoint_to_instance(instance=instance, edge=edge))
    return new_point_ids

def _normalize_edge(edge: Edge) -> Edge:
    a, b = edge
    return (min(a, b), max(a, b))

def _normalize_edges(edges: List[Edge]) -> List[Edge]:
    return [normalize_edge(edge) for edge in edges]

def tour_difference(old_tour: Tour, new_tour: Tour) -> Tuple[List[Edge], List[Edge]]:
    old_edges = set(_normalize_edges(get_edges_from_tour(old_tour)))
    new_edges = set(_normalize_edges(get_edges_from_tour(new_tour)))
    deleted_edges = []
    for old_edge in old_edges:
        if old_edge not in new_edges:
            deleted_edges.append(old_edge)
    added_edges = []
    for new_edge in new_edges:
        if new_edge not in old_edges:
            added_edges.append(new_edge)
    assert(len(deleted_edges) == len(added_edges))
    return deleted_edges, added_edges

def disjoin_edges(edges: List[Edge]):
    point_sets = {0: set()}
    edge_sets = {0: []}
    for edge in edges:
        a, b = edge
        added = False
        for set_id in point_sets:
            point_set = point_sets[set_id]
            if a in point_set or b in point_set:
                point_sets[set_id].add(a)
                point_sets[set_id].add(b)
                edge_sets[set_id].append(edge)
                added = True
                break
        if not added:
            new_set_id = len(point_sets)
            point_sets[new_set_id] = set()
            point_sets[new_set_id].add(a)
            point_sets[new_set_id].add(b)
            edge_sets[new_set_id] = [edge]
    return list(edge_sets.values())
