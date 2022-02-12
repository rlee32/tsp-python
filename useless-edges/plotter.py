#!/usr/bin/env python3

from matplotlib import pyplot as plt

def plot_points(points, style='x'):
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    plt.plot(x, y, style)

def plot_tour(points, tour, linestyle='-'):
    x = [points[t - 1][0] for t in tour]
    y = [points[t - 1][1] for t in tour]
    n = len(points)
    x.append(x[0])
    y.append(y[0])
    plt.plot(x, y, linestyle)

def show():
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

import sys
import reader

if __name__ == '__main__':
    print("inputs: instance_path optional_tour_path")
    instance = reader.read_instance(sys.argv[1])
    print(f"instance count: {len(instance)}")
    plot_points(instance)
    if len(sys.argv) > 2:
        tour = reader.read_tour(sys.argv[2])
        print(f"tour count: {len(tour)}")
        plot_tour(instance, tour)
    show()
