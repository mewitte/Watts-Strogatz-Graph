import logging
import math
import matplotlib.pyplot as plt
import networkx as nx
from pathlib import Path
import random
import sys

class RandomGraph:
  def __init__(self, n, p):
    self._create_random_graph(n, p)
    while not nx.is_connected(self._random_graph):
      logging.error("Graph is not connected! Creating new graph")
      self._create_random_graph(n, p)
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
    
  def _create_random_graph(self, n, p):
    self._random_graph = nx.Graph()
    self._random_graph.add_nodes_from(range(0, n))
    for i in self._random_graph.nodes:
      for j in self._random_graph.nodes:
        if i != j and random.random() < p:
          self._random_graph.add_edge(i, j)

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
      self._random_graph.nodes[node]["clustering_coefficient"] = triangles / neighbor_pairs

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

if __name__ == "__main__":
  directory = sys.argv[1]
  Path(f"./{directory}").mkdir(parents=True, exist_ok=True)
  logging.basicConfig(
    filename=f"./{directory}/gg.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
  )

  # experiment for dependency between growth of node number and average path length
  # n is starting number of nodes, p is starting probability for an edge between nodes
  # c refers to different values for n
  # between each iteration, the value of n is multiplied by 2, p is adapted accordingly
  # getting the cluster coefficient for large values for n takes a long time, it might be best to comment that out for this experiment
  n = 32
  p = 0.3
  path_lengths = []
  nodes = []
  for c in range(0, 10):
    logging.info(f"Creating graph with n={n} and p={p}")
    graph = RandomGraph(n, p)
    logging.info(f"Average path length: {graph.average_path_length}")
    nodes.append(n)
    path_lengths.append(graph.average_path_length)
    p = p * (n - 1) / (n * 2 - 1)
    n = n * 2
  plt.plot(nodes, path_lengths)
  plt.xlabel("Number of nodes")
  plt.ylabel("Average path length")
  plt.savefig(f"./{directory}/path_lengths.png")

  # experiment for the depenency between n and the clustering coefficient
  nodes = [32, 64, 128, 256, 512, 1024, 2048, 4096]
  p = 0.3
  clustering_coefficients = []
  for n in nodes:
    average = 0
    for _ in range(0, 1):
      logging.info(f"Creating graph with n={n} and p={p}")
      graph = RandomGraph(n, p)
      logging.info(f"Clustering coefficient: {graph.clustering_coefficient}")
      average += graph.clustering_coefficient
    clustering_coefficients.append(graph.clustering_coefficient / 10)
  plt.plot(nodes, clustering_coefficients)
  plt.xlabel("Number of nodes")
  plt.ylabel("Clustering coefficient")
  plt.savefig(f"./{directory}/clustering_coefficients_n.png")

  # experiment for the dependencz between p and the clustering coefficient
  n = 512
  p = 0.05
  probabilities = []
  clustering_coefficients = []
  while p <= 0.95 :
    average = 0
    logging.info(f"Creating graph with n={n} and p={p}")
    graph = RandomGraph(n, p)
    logging.info(f"Clustering coefficient: {graph.clustering_coefficient}")
    average += graph.clustering_coefficient
    probabilities.append(p)
    clustering_coefficients.append(graph.clustering_coefficient)
    p = round(p + 0.05, 2)
  plt.plot(probabilities, clustering_coefficients)
  plt.xlabel("Probability")
  plt.ylabel("Clustering coefficient")
  plt.savefig(f"./{directory}/clustering_coefficients_p.png")
