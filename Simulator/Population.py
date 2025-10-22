import networkx as nx
import random
from EnumeratedTypes import State
from Person import Person

class Population:
    """ Represents the population and manages infection spread."""

    def __init__(self, size, avg_degree, rewire_prob, risk_factors = None):
        """ Initialize the population network."""

        self.size = size
        self.avg_degree = avg_degree
        self.rewire_prob = rewire_prob
        self.risk_factors = risk_factors
        self.population = [Person() for _ in range(size)]
        
        # Creates a small-world network for realistic contacts
        self.network = nx.watts_strogatz_graph(size, avg_degree, rewire_prob)

        # Base contact rate (modifiable by social distancing)
        self.contact_reduction = 1.0

    def adjust_contact_rate(self, reduction_factor):
        """ Reduce contact rate due to social distancing."""

        self.contact_reduction = max(0.0, 1.0 - reduction_factor)

    def update(self, virus, day):
        """ Update infection states across the population."""

        newly_exposed = []
        newly_infected = []
        newly_recovered = []

        for person in self.population:

            # Skip isolated or recovered individuals
            if person.isolated or person.state == State.RECOVERED:
                continue

            # Controls infection spread and will control Susceptible to Exposed
            if person.state == State.SUSCEPTIBLE:
                neighbors = [self.population[n] for n in self.network.neighbors(person.id)]
                infected_neighbors = [n for n in neighbors if n.state == State.INFECTED]
                
                if infected_neighbors:
                    infection_prob = virus.infect_rate * self.contact_reduction
                    
                    # Adjust infection rates based on risk groups
                    if self.risk_factors:
                        risk_factor = self.risk_factors.get(person.age_group, 1.0)
                        infection_prob *= risk_factor

                    if random.random() < infection_prob:
                        newly_exposed.append(person)

            # Controls infection spread and will control Exposed to Infected
            elif person.state == State.EXPOSED:
                person.days_exposed += 1
                if person.days_exposed >= virus.infection_time:
                    newly_infected.append(person)

            # Recovers person based on cure rate and will control Infected to Recovered
            elif person.state == State.INFECTED:
                person.days_infected += 1
                if random.random() < virus.cure_rate:
                    newly_recovered.append(person)

        # Apply transitions after iteration
        for p in newly_exposed:
            p.expose(day)
        for p in newly_infected:
            p.infect(day)
        for p in newly_recovered:
            p.recover()