# pis2grafy

A simple Python module made specifically for solving an assignment
for project's task organization and timing
that is a part of "Information Systems Design 2" (PIS2) course on
University of Finance and Administration, department of
Informatics and Mathematics. Released publicly as open-source
software under MIT license (without only sample assignment data).

The program takes a graph in matrix (tabular) format
(where rows and columns are nodes and intersecting numbers
other than 0 mean there is a connection between those
nodes of a given weight), parses them and finds the longest weighted path
(a project's "critical path"). Next, the graph is traversed forwards,
marking earliest possible starting times and finish times, then traversing
backwards and filling in latest possible finish and start times.


## Requirements
 
 - Python 3 (developed and tested on 3.6)
 - [GraphViz](https://www.graphviz.org/) installed - it should be in your distro's repositories
 - Installing Python dependencies from requirements.txt (if you have [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)) installed you can just run `make`)
 
Python dependencies include [networkx](https://networkx.github.io/) that does the majority of work
holding the graphs, allowing us to traverse them, set attributes and such;
and [pygraphviz](https://pygraphviz.github.io/) that is used to generate
.dot files and communicate with GraphViz for drawing the graphs into actual images.
 

## Usage

Either *run the Makefile* (`make init` installs dependencies,
`make run` runs the module and `make clean` cleans the output directory)
or *run the module directly*.

To supply your own data put it in `data.py` in the `data` dictionary.
By default the first line and column of every data set is discarded.


## Example

Given this input data:

```python
data = [
    """Node       1   2    3   4    5    6
    1             0   8    0   2    7    3
    2             0   0    2   4    0    8
    3             0   0    0   6    18   12
    4             0   0    0   0    8    3
    5             0   0    0   0    0    6
    6             0   0    0   0    0    0 """,
]
```

You can expect output such as this:
```
Graph 0
Longest path: [1, 2, 3, 5, 6]
Path length: 34
Writing ../output/0
Graph 0 done.
```

And three generated files - a .dot source file for [GraphViz](https://www.graphviz.org/),
a .csv file with tabular result showing all computed values
and a .png file with the graph drawn out.

The generated graph could look something like this:

![Example graph image](/example_graph.png?raw=true)
