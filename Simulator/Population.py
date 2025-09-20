import networkx as nx
from Person import Person

class Population:
    def __init__(self, size: int):
        self.population = [Person() for _ in range(size)]
        self.networkX = nx.erdos_renyi_graph(size, 0.1)
        self.node_to_person = {i: self.population[i] for i in range(size)}

    def generate(self):
        size = len(self.population)
        self.population = [Person() for _ in range(size)]
        self.networkX = nx.erdos_renyi_graph(size, 0.1)
        self.node_to_person = {i: self.population[i] for i in range(size)}
    
    def get_contacts(self, person: Person):
        idx = self.population.index(person)
        neighbors = self.networkX.neighbors(idx)
        return [self.node_to_person[n] for n in neighbors]