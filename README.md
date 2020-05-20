# Wattz-Strogatz-Graph

## Installation
* `sudo apt install python3 python3-pip pipenv`
* `pipenv shell`
* `pipenv install`

## Usage
Whenever you enter, run `pipenv shell` to get the pipenv dependencies. Call `python3 gilbert_graph.py path/to/dir/` to run an experiment on the average path length of graphs with rising number of nodes. It will save the output diagram to the specified path, together with a log file. 

## Development
To create a Wattz-Strogatz random graph, just call `RandomGraph(n, k, p)`. The average path length will then be saved as `graph.average_path_length`, the clustering coefficient will be saved as `graph.clustering_coefficient`. These values are lazy intialized, so that only the computation for the needed metrics are done.

For comparison, you can call `graph.get_average_path_length()` and `graph.get_clustering_coefficient()`, which calls the NetworkX alogrithms for the problem. Note that for big values for n, the operations will take some time. The average degree is saved as `graph.average_degree`. You can use `tail -f path/gg.log` to get quasi output for the logging.
