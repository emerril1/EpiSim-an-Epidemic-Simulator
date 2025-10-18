import networkx as nx
import random
from Person import Person
from EnumeratedTypes import State

class Population:
    """Manages the population and infection spread through contacts."""

    def __init__(self, size, avg_degree, rewire_prob):
        self.size = size
        self.population = [Person(i) for i in range(size)]
        self.graph = nx.watts_strogatz_graph(size, avg_degree, rewire_prob)
        for i, person in enumerate(self.population):
            person.id = i
        self.contact_reduction = 0.0  # for social distancing

    def get_contacts(self, person):
        return [self.population[n] for n in self.graph.neighbors(person.id)]

    def adjust_contact_rate(self, reduction):
        """Reduce contact probability for social distancing."""
        self.contact_reduction = reduction

    def update(self, virus, current_day):
        """Simulate one day of infections and recoveries."""
        new_exposures = []
        new_infections = []
        new_recoveries = []

        for person in self.population:
            if person.state == State.INFECTED and not getattr(person, "isolated", False):
                for contact in self.get_contacts(person):
                    if contact.state == State.SUSCEPTIBLE:
                        infection_prob = virus.infect_rate * (1 - self.contact_reduction)
                        if contact.vaccinated:
                            infection_prob *= (1 - contact.vaccine_effectiveness)
                        if random.random() < infection_prob:
                            new_exposures.append(contact)

                if random.random() < virus.cure_rate:
                    new_recoveries.append(person)

            elif person.state == State.EXPOSED:
                if (current_day - person.exposed_time) >= virus.infection_time:
                    new_infections.append(person)

        for p in new_exposures:
            p.expose(current_day)
        for p in new_infections:
            p.infect(current_day)
        for p in new_recoveries:
            p.recover()