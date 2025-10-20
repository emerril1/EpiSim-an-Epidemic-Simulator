import networkx as nx
import random
from Person import Person
from EnumeratedTypes import State

class Population:
    """Manages individuals and their contact network."""

    def __init__(self, size, avg_degree, rewire_prob, risk_factors = None):
        self.size = size
        self.avg_degree = avg_degree
        self.rewire_prob = rewire_prob
        self.population = [Person(i) for i in range(size)]
        self.graph = nx.watts_strogatz_graph(size, avg_degree, rewire_prob)
        self.risk_factors = risk_factors

    def get_contacts(self, person):
        """ Get contacts of a person based on the contact network."""

        neighbors = list(self.graph.neighbors(person.id))
        return [self.population[n] for n in neighbors]

    def update(self, virus, current_day):
        """ Update the state of the population for one time step."""

        new_exposures, new_infections, new_recoveries = [], [], []

        # Process each person in the population
        for person in self.population:
            if person.state == State.INFECTED:
                for contact in self.get_contacts(person):
                    if contact.state == State.SUSCEPTIBLE:
                        infection_prob = virus.infect_rate

                        # Apply risk group modifier from config
                        group = contact.age_group
                        if group in self.risk_factors:
                            infection_prob *= self.risk_factors[group]

                        # Apply vaccine protection if vaccinated
                        if contact.vaccinated:
                            infection_prob *= (1 - contact.vaccine_effectiveness)

                        if random.random() < infection_prob:
                            new_exposures.append(contact)

                # Recovery chance
                if random.random() < virus.cure_rate:
                    new_recoveries.append(person)

            elif person.state == State.EXPOSED:
                if (current_day - person.exposed_time) >= virus.infection_time:
                    new_infections.append(person)

        # Apply state changes
        for p in new_exposures:
            p.expose(current_day)
        for p in new_infections:
            p.infect(current_day)
        for p in new_recoveries:
            p.recover()