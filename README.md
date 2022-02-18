# tsp-python
Monorepo for Euclidean, symmetric Traveling Salesman Problem solvers written in Python.

# Organization
Each folder contains a solver. I am not sure how to elegantly import modules from parent directories, so common modules are simply copied into every folder in which they are used.

# Input / Output Format
Inputs (tour files, problem instance files) are in TSPLIB format.

# TSP Problem Instances
Small problems for quick testing are stored in 'data/' for convenience.

More problems can be found at:
https://www.math.uwaterloo.ca/tsp/vlsi/index.html

# Folder Descriptions

mst: functions to make minimum spanning trees.

useless-edges: functions to identify useless edges.

tsp_plot: functions to plot TSP instances and edges.

2-opt: simple 2-opt hill climbing solver (quadratic work complexity).

instance_buildup: solver in which 2-opt is applied to growing instance size.
