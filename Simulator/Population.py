import networkx as nx
from Person import Person

# Class representing a population of people and their contact network. 
# Uses an Erdős-Rényi graph to model random connections between individuals.

class Population:
    # Initialize the population with a given size. Create people and a contact network.
    def __init__(self, size: int):
        self.population = [Person() for _ in range(size)]
        self.networkX = nx.erdos_renyi_graph(size, 0.1)
        self.node_to_person = {i: self.population[i] for i in range(size)}

    # Rebuild a new population and contact network when needed. 
    def generate(self):
        size = len(self.population)
        self.population = [Person() for _ in range(size)]
        self.networkX = nx.erdos_renyi_graph(size, 0.1)
        self.node_to_person = {i: self.population[i] for i in range(size)}

    # Get the contacts of a given person based on the network.
    def get_contacts(self, person: Person):
        idx = self.population.index(person)
        neighbors = self.networkX.neighbors(idx)
        return [self.node_to_person[n] for n in neighbors]