#!/usr/bin/env python3

from typing import Tuple, List, Set, Optional
from tsp_types import Instance, Tour, Edge, Dict
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
    return [_normalize_edge(edge) for edge in edges]

def tour_difference(old_tour: Tour, new_tour: Tour) -> Tuple[List[Edge], List[Edge]]:
    old_edges = set(_normalize_edges(get_edges_from_tour(old_tour)))
    new_edges = set(_normalize_edges(get_edges_from_tour(new_tour)))
    deleted_edges = set()
    for old_edge in old_edges:
        if old_edge not in new_edges:
            deleted_edges.add(old_edge)
    added_edges = set()
    for new_edge in new_edges:
        if new_edge not in old_edges:
            added_edges.add(new_edge)
    for edge in deleted_edges:
        assert(edge not in added_edges)
    for edge in added_edges:
        assert(edge not in deleted_edges)
    assert(len(deleted_edges) == len(added_edges))
    return deleted_edges, added_edges

def _map_points_to_edges(edges: List[Edge]) -> Dict[int, Set[Edge]]:
    edges = _normalize_edges(edges)
    points_to_edges = {}
    for edge in edges:
        for p in edge:
            if p not in points_to_edges:
                points_to_edges[p] = set()
            points_to_edges[p].add(edge)
    for p in points_to_edges:
        assert(len(points_to_edges[p]) in (2, 4))
    return points_to_edges

def disjoin_edge_set(edges: List[Edge]) -> Tuple[Set[Edge], List[Edge]]:
    """Extracts one disjoint set of edges. Returns one disjoint set and the rest. """
    points_to_edges = _map_points_to_edges(edges=edges)
    edge_set = set()
    seen = set()
    to_explore = [next(iter(points_to_edges))]
    while to_explore:
        p = to_explore.pop()
        adjacent = points_to_edges[p]
        seen.add(p)
        for edge in adjacent:
            edge_set.add(edge)
            for p in edge:
                if p not in seen:
                    to_explore.append(p)
    remaining_edges = []
    for edge in edges:
        if edge not in edge_set:
            remaining_edges.append(edge)
    return edge_set, remaining_edges

def disjoin_edge_sets(edges: List[Edge]) -> List[List[Edge]]:
    if not edges:
        return []
    edge_set, remaining_edges = disjoin_edge_set(edges)
    edge_sets = [edge_set]
    while remaining_edges:
        edge_set, remaining_edges = disjoin_edge_set(remaining_edges)
        edge_sets.append(edge_set)
    return edge_sets

def get_kmoves_between_tours(old_tour: Tour, new_tour: Tour) -> List[List[Edge]]:
    deleted, added = tour_difference(old_tour=old_tour, new_tour=new_tour)
    edge_sets = disjoin_edge_sets(list(deleted) + list(added))
    kmoves = []
    for edge_set in edge_sets:
        kmoves.append([[], []])
        for edge in edge_set:
            if edge in deleted:
                kmoves[-1][0].append(edge)
            else:
                kmoves[-1][1].append(edge)
        assert(len(kmoves[-1][0]) == len(kmoves[-1][1]))
    return kmoves

def kmove_gain(instance: Instance, kmove: List[List[Edge]]) -> int:
    total = 0
    for deleted in kmove[0]:
        total += distance(instance=instance, a=deleted[0], b=deleted[1])
    for added in kmove[1]:
        total -= distance(instance=instance, a=added[0], b=added[1])
    return total

def apply_kmove(tour: Tour, kmove: List[List[Edge]]) -> Optional[Tour]:
    edges = get_edges_from_tour(tour=tour)
    edges = set(_normalize_edges(edges))
    for edge in kmove[0]:
        edges.remove(edge)
    for edge in kmove[1]:
        edges.add(edge)
    points_to_edges = _map_points_to_edges(edges=edges)
    for p in points_to_edges:
        points_to_edges[p] = list(points_to_edges[p])
        assert(len(points_to_edges[p]) == 2)
    prev = next(iter(points_to_edges))
    current = points_to_edges[prev][0][0] if points_to_edges[prev][0][0] != prev else points_to_edges[prev][0][1]
    first = prev
    new_tour = [prev]
    while current != first:
        new_tour.append(current)
        prev_edge = _normalize_edge((current, prev))
        next_edge = points_to_edges[current][0]
        if prev_edge == next_edge:
            next_edge = points_to_edges[current][1]
        assert(prev_edge in points_to_edges[current])
        new_prev = current
        current = next_edge[0] if next_edge[0] != current else next_edge[1]
        prev = new_prev
    if len(tour) == len(new_tour):
        return new_tour
