from EnumeratedTypes import State, InterventionType
import random
from Population import Population

''' Different types of interventions to control the spread of the virus.
Can either vaccinate a portion of the population or quarantine infected individuals.'''

class Intervention:
    ''' Initialize with the type of intervention.'''
    def __init__(self, intervention_type: InterventionType):
        self.type = intervention_type
    
    ''' Execute the intervention type on the given population.'''
    def execute(self, population: Population):
        if self.type == InterventionType.VACCINE:
            for person in random.sample(population.population, len(population.population) // 30):
                if person.state == State.SUSCEPTIBLE:
                    person.state = State.RECOVERED
        elif self.type == InterventionType.QUARANTINE:
            infected_ids = [p.id - 1 for p in population.population if p.state == State.INFECTED]
            population.networkX.remove_nodes_from(infected_ids)
