import networkx as nx
from Person import Person

class Population:
    ''' Class representing a population of people and their contact network. 
        Uses an Erdős-Rényi graph to model random connections between individuals. e.g. contact patterns.'''
    
    def __init__(self, size: int):
        ''' Initialize the population with a given size. Create people and a contact network.'''
        
        self.population = [Person() for _ in range(size)]
        self.networkX = nx.erdos_renyi_graph(size, 0.1)
        self.node_to_person = {i: self.population[i] for i in range(size)}

    def generate(self):
        ''' Rebuild a new population and contact network when needed.'''
        
        size = len(self.population)
        self.population = [Person() for _ in range(size)]
        self.networkX = nx.erdos_renyi_graph(size, 0.1)
        self.node_to_person = {i: self.population[i] for i in range(size)}

    def get_contacts(self, person: Person):
        ''' Get the contacts of a given person based on the network.'''
        
        idx = self.population.index(person)
        neighbors = self.networkX.neighbors(idx)
        return [self.node_to_person[n] for n in neighbors]
