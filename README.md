# Gilbert-Graph

## Installation
* `sudo apt install python3 python3-pip`
* `pipenv install`

## Usage
Whenever you enter, run `pipenv shell` to get the pipenv dependencies. Call `python3 gilbert_graph.py path/to/dir/` to run an experiment on the average path length of graphs with rising number of nodes. It will save the output diagram to the specified path, together with a log file. 

## Development
To create a Gilbert random graph, just call `RandomGraph(n, p)`. The average path length will then be saved as `graph.average_path_length`, the clustering coefficient will be saved as `graph.clustering_coefficient`. For comparison, you can call `graph.get_average_path_length()` and `graph.get_clustering_coefficient()`, which calls the NetworkX alogrithms for the problem. Note that for big values for n, getting the average path length will take some time. The average degree is saved as `graph.average_degree`. You can use `tail -f path/gg.log` to get quasi output for the logging.
