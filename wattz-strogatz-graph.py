import logging
import matplotlib.pyplot as plt
import networkx as nx
from pathlib import Path
import random
import sys

class RandomGraph:
  def __init__(self, n, k, p):
    self._create_random_graph(n, k, p)
    while not nx.is_connected(self._random_graph):
      logging.error("Graph is not connected! Creating new graph")
      self._create_random_graph(n, k, p)
    self._average_path_length = False
    self._clustering_coefficient = False
    self._average_degree = False

  @property
  def average_path_length(self):
    if not self._average_path_length:
      self._compute_average_path_length()
    return self._average_path_length

  @property
  def clustering_coefficient(self):
    if not self._clustering_coefficient:
      self._compute_clustering_coefficient()
    return self._clustering_coefficient

  @property
  def average_degree(self):
    if not self._average_degree:
      self._compute_average_degree
    return self._average_degree

  def _add_paths(self, k, p):
    for index, node in enumerate(list(self._random_graph.nodes)):
      for i in range(1, k + 1):
        target_index = (index + i - len(self._random_graph.nodes), index + i)[i >= len(self._random_graph)]
        if random.random() < p:
          while True: # do for do-while
            target_index = random.randint(0, len(self._random_graph) - 1)
            if index != target_index: # while for do-while
              break
        self._random_graph.add_edge(node, list(self._random_graph.nodes)[target_index])
   
  def _create_random_graph(self, n, k, p):
    self._random_graph = nx.Graph()
    self._random_graph.add_nodes_from(range(0, n))
    self._add_paths(k, p)

  def _get_sample_paths(self):
    node_count = len(self._random_graph)
    sample_paths = []
    if node_count <= 14: # with 14 nodes, there are a maximum of 91 node combinations possible, 15 has 105
      for node1 in list(self._random_graph.nodes):
        for node2 in list(self._random_graph.nodes):
          if (
            node1 != node2
            and (node1, node2) not in sample_paths
            and (node2, node1) not in sample_paths
          ):
            sample_paths.append((node1, node2))
    else:
      while len(sample_paths) < 100:
        random_node1 = list(self._random_graph.nodes)[random.randint(0, node_count - 1)]
        random_node2 = list(self._random_graph.nodes)[random.randint(0, node_count - 1)]
        if (
          random_node1 != random_node2
          and (random_node1, random_node2) not in sample_paths
          and (random_node2, random_node1) not in sample_paths
        ):
          sample_paths.append((random_node1, random_node2))
    return sample_paths

  def _compute_average_path_length(self):
    sample_paths = self._get_sample_paths()
    distances = []
    for (first_node, second_node) in sample_paths:
      distances.append(nx.shortest_path_length(self._random_graph, first_node, second_node))
    self._average_path_length = sum(distances) / len(distances)

  def _compute_node_clustering_coefficients(self):
    for node in list(self._random_graph.nodes):
      triangles = 0
      neighbor_pairs = 0
      neighbors = list(self._random_graph.neighbors(node))
      for neighbor1 in neighbors:
        for neighbor2 in neighbors:
          if neighbor1 == neighbor2:
            continue
          neighbor_pairs += 1
          if self._random_graph.has_edge(neighbor1, neighbor2):
            triangles += 1
      self._random_graph.nodes[node]["clustering_coefficient"] = (triangles / neighbor_pairs, 0)[neighbor_pairs == 0]

  def _compute_clustering_coefficient(self):
    self._compute_node_clustering_coefficients()
    clustering_coefficients = []
    for (_, coefficient) in list(self._random_graph.nodes.data("clustering_coefficient")):
      clustering_coefficients.append(coefficient)
    self._clustering_coefficient = sum(clustering_coefficients) / len(clustering_coefficients)

  def _compute_average_degree(self):
    degrees = []
    for (_, degree) in list(self._random_graph.degree):
      degrees.append(degree)
    self._average_degree = sum(degrees) / len(degrees)

  def get_average_path_length(self):
    return nx.average_shortest_path_length(self._random_graph)

  def get_clustering_coefficient(self):
    return nx.average_clustering(self._random_graph)

def create_plot(path, x, y, x_label, y_label):
  plt.plot(x, y)
  plt.xlabel(x_label)
  plt.ylabel(y_label)
  plt.xscale("log")
  plt.savefig(path)
  plt.close()

if __name__ == "__main__":
  directory = sys.argv[1]
  Path(f"./{directory}").mkdir(parents=True, exist_ok=True)
  logging.basicConfig(
    filename=f"./{directory}/wsg.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
  )

  # experiment from exercise 4
  n = 5000
  k = 2
  probabilities = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1]
  path_lengths = []
  clustering_coefficients = []
  for p in probabilities:
    logging.info(f"Creating graph with n={n}, k={k} and p={p}")
    graph = RandomGraph(n, k, p)
    logging.info(f"Average path length: {graph.average_path_length}")
    path_lengths.append(graph.average_path_length)
    logging.info(f"Clustering coefficient: {graph.clustering_coefficient}")
    clustering_coefficients.append(graph.clustering_coefficient)
  create_plot(
    f"./{directory}/clustering_coefficient.png",
    probabilities,
    clustering_coefficients,
    "p",
    "clustering coefficient"
  )
  create_plot(
    f"./{directory}/path_lengths.png",
    probabilities,
    path_lengths,
    "p",
    "average path length"
  )
