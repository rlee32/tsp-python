#!/usr/bin/env python3

from matplotlib import pyplot as plt
from typing import Dict, Tuple, List

Instance = Dict[int, Tuple[float, float]]
Tour = List[int]
Edge = Tuple[int, int]

def plot_point_by_id(instance: Instance, point_id: int, style='x', show=True):
    p = instance[point_id]
    x = p[0]
    y = p[1]
    plt.plot(x, y, style)
    if show:
        show_plot()

def plot_points_by_ids(instance: Instance, point_ids: List[int], style='x', show=True):
    for point_id in point_ids:
        plot_point_by_id(instance=instance, point_id=point_id, style=style, show=show)

def plot_points_by_instance(instance: Instance, style='x', show=True):
    points = list(instance.values())
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    plt.plot(x, y, style)
    if show:
        show_plot()

def plot_tour(instance: Instance, tour: Tour, linestyle='-', show=True):
    x = [instance[a][0] for a in tour]
    y = [instance[a][1] for a in tour]
    n = len(instance)
    x.append(x[0])
    y.append(y[0])
    plot_points(instance=instance, style='x', show=False)
    plt.plot(x, y, linestyle)
    if show:
        show_plot()

def plot_edge(instance: Instance, edge: Edge, linestyle=':', show=True):
    a, b = edge
    x = [instance[a][0], instance[b][0]]
    y = [instance[a][1], instance[b][1]]
    plt.plot(x, y, linestyle)
    if show:
        show_plot()

def show_plot():
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

import sys
from tsp_reader import read_instance, read_tour

if __name__ == '__main__':
    print("inputs: instance_path optional_tour_path")
    instance = read_instance(sys.argv[1])
    print(f"instance count: {len(instance)}")
    plot_points_only = len(sys.argv) == 2
    if plot_points_only:
        plot_points(instance=instance, style='x')
    else:
        tour = read_tour(sys.argv[2])
        print(f"tour count: {len(tour)}")
        plot_tour(instance=instance, tour=tour)
