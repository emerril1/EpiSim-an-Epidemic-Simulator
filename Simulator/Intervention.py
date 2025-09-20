from EnumeratedTypes import State, InterventionType
import random
from Population import Population

class Intervention:
    def __init__(self, intervention_type: InterventionType):
        self.type = intervention_type
    
    def execute(self, population: Population):
        if self.type == InterventionType.VACCINE:
            for person in random.sample(population.population, len(population.population) // 10):
                if person.state == State.SUSCEPTIBLE:
                    person.state = State.RECOVERED
        elif self.type == InterventionType.QUARANTINE:
            infected_ids = [p.id - 1 for p in population.population if p.state == State.INFECTED]
            population.networkX.remove_nodes_from(infected_ids)