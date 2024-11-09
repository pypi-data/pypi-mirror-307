ant_colony_algorithm = """
from networkx.algorithms.centrality.current_flow_betweenness_subset import edge_current_flow_betweenness_centrality_subset
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

def plot_graph(
    g,
    title = " ",
    highlight_edges = [],
    ):

    pos = nx.get_node_attributes(g, "pos")

    plt.figure(figsize=(17, 17))
    plt.title(title)
    nx.draw(g, pos=pos, labels={x: x for x in g.nodes}, width=2)
    weights = nx.get_edge_attributes(g, "weight")
    # Draw edge labels
    nx.draw_networkx_edge_labels(g, pos, edge_labels=weights, label_pos=.4)
    # Highlight edges
    nx.draw_networkx_edges(g, pos, edgelist=highlight_edges, edge_color="r")

    nx.draw_networkx_edge_labels(
        g,
        pos,
        edge_labels={
            e:w
            for e, w in weights.items()
            if e in map(lambda x: tuple(sorted(x)), highlight_edges)
        },
        font_color="r",
        label_pos=.4
    )

    plt.show()

def generate_random_weighted_graph(n, low, high):
    g = nx.generators.complete_graph(n)

    g.add_weighted_edges_from([
        (u, v, np.random.randint(low, high))
        for u, v in g.edges()
    ])

    nx.set_node_attributes(g, nx.spring_layout(g), "pos")

    return g

def zero_divide(a, b):
    return np.divide(a, b, out=np.zeros_like(a), where=b!=0)


class ACOTSP:
    def __init__(self, g, n_ants=100, alpha=1, beta=5, Q=100, rho=.6):
        self.g = g
        self.n_nodes = g.number_of_nodes()

        distances = nx.to_numpy_array(g)
        print(distances)

        self.visibility = zero_divide(np.ones_like(distances), distances)

        self.n_ants = n_ants
        self.alpha = alpha
        self.beta = beta

        self.Q = Q
        self.rho = rho

        self.pheromone = np.ones((self.n_nodes, self.n_nodes))


    def compute_probabilities(self, visited):
        self.prob = self.pheromone ** self.alpha * self.visibility ** self.beta

        self.prob[:, np.array(list(visited))] = 0

        prob_sum = self.prob.sum(-1, keepdims = True)

        self.prob = zero_divide(self.prob, prob_sum)

        return self.prob

    def initialize_ants(self):
        nodes = list(self.g.nodes)

        self.ant_pos = np.random.choice(nodes, self.n_ants)


    def path_length(self, path):
        edge_weights = nx.get_edge_attributes(self.g, "weight")

        return sum(edge_weights[tuple(sorted(edge))] for edge in path)

    def ant_tour(self, k):
        current = self.ant_pos[k]

        visited = [current]
        path = []

        self.compute_probabilities(visited)

        while True:
            prev = int(current)

            current = np.random.choice(self.n_nodes, p = self.prob[current])

            visited.append(current)
            path.append((prev, current))
            if np.all(self.prob[current] == 0):
                break

            self.compute_probabilities(visited)

        self.paths[k] = path

    def update_pheromone(self):
        d_pheromone = np.zeros((self.n_nodes, self.n_nodes, self.n_ants))

        for k, path in enumerate(self.paths):
            if len(path) == self.n_nodes - 1:
                for u, v in path:
                    d_pheromone[u, v, k] = d_pheromone[v, u, k] = self.Q / self.path_length(path)

        d_pheromone = d_pheromone.sum(-1)
        self.pheromone = self.rho * self.pheromone + d_pheromone

    def run(self, n_iter = 1):
        self.initialize_ants()
        self.min_path = None
        for t in range(n_iter):
            self.paths = [[None]] * self.n_ants

            for k in range(self.n_ants):
                self.ant_tour(k)

            self.update_pheromone()

            self.hamiltonian_paths = [
                path
                for path in self.paths
                if len(path) == self.n_nodes - 1
            ]


            if t % 10 == 0:
                print(f"Iteration {t}: Best path: {self.best_path} with length {self.best_path_length}")


    @property
    def best_path_length(self):
        return self.path_length(self.best_path)

    @property
    def best_path(self):
        if not hasattr(self, "hamiltonian_paths") or len(self.hamiltonian_paths) == 0:
            return None
        return min(self.hamiltonian_paths if self.min_path is None else [self.min_path, *self.hamiltonian_paths] , key=self.path_length)



g = generate_random_weighted_graph(4, 10, 50)


acotsp_solver = ACOTSP(g, n_ants=100, alpha=1, beta=5, Q=100, rho=.4)

acotsp_solver.run(100)

plot_graph(g, "Shortest Path found by ACO for TSP", acotsp_solver.best_path)
"""