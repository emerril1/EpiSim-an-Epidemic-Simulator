import networkx as nx
import random
from Person import Person

class Population:
    ''' Class representing the population in the simulation.
        Manages individuals and their contact network.'''

    def __init__(self, size, avg_degree, rewire_prob):
        self.size = size
        self.avg_degree = avg_degree
        self.rewire_prob = rewire_prob
        self.population = [Person(i) for i in range(size)]

        # Small-world network: each person connected to k neighbors
        self.graph = nx.watts_strogatz_graph(size, avg_degree, rewire_prob)

        # Assign IDs
        for i, person in enumerate(self.population):
            person.id = i

    def get_contacts(self, person):
        """ Function to get contacts of a person based on the network graph. """

        neighbor_ids = list(self.graph.neighbors(person.id))
        return [self.population[n] for n in neighbor_ids]
