#!/usr/bin/env python3

import tsp_io
import tsp_plot
import sys

if __name__ == "__main__":
    instance = tsp_io.read_instance(path=sys.argv[1])
    opt = tsp_io.read_tour(path=sys.argv[2])
    other = tsp_io.read_tour(path=sys.argv[3])
    tsp_plot.plot_tour(instance=instance, tour=opt, linestyle="b:", show=False)
    tsp_plot.plot_tour(instance=instance, tour=other, linestyle="r:")
