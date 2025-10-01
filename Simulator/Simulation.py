from Population import Population
from Virus import Virus
from Intervention import Intervention 
from EnumeratedTypes import State
from EnumeratedTypes import InterventionType
import networkx as nx
import random

# Main simulation class that runs the epidemic simulation.
# Tracks the state of the population over time and applies virus dynamics.

class Simulation:
    # Initialize with a population and a virus.
    def __init__(self, population: Population, virus: Virus):
        self.population = population
        self.virus = virus
        self.time = 0
        self.history = {}

    # Perform a single time step in the simulation.
    def step(self):
        new_infections= []
        for person in self.population.population:
            if person.state == State.INFECTED:
                for contact in self.population.get_contacts(person):
                    if contact.state == State.SUSCEPTIBLE and random.random() < self.virus.infect_rate:
                        new_infections.append(contact)
                if random.random() < self.virus.cure_rate:
                    person.cure(self.time)

        for p in new_infections:
            p.infect(self.time)

        self.track_stats()
        self.time += 1

    # Run the simulation for a specified number of steps.
    def run(self, num_of_steps: int):
        for _ in range (num_of_steps):
            self.step()

    # Track the number of susceptible, infected, and recovered individuals.
    def track_stats(self):
        counts = {
            "S": sum(1 for p in self.population.population if p.state == State.SUSCEPTIBLE),
            "I": sum(1 for p in self.population.population if p.state == State.INFECTED),
            "R": sum(1 for p in self.population.population if p.state == State.RECOVERED)
        }
        self.history[self.time] = counts

# Main execution block to run a sample simulation.

if __name__ == "__main__":
    pop = Population(size = 50)
    vir = Virus("Virus", infect_rate = 0.2, cure_rate = 0.05)
    sim = Simulation(pop, vir)

    # Infect a random individual at the start of the simulation.
    patient_zero = random.choice(pop.population)
    patient_zero.infect(time = 0)

    ## vaccine = Intervention(InterventionType.VACCINE)
    ## vaccine.execute(pop)

    quarantine = Intervention(InterventionType.QUARANTINE)
    quarantine.execute(pop)

    sim.run(20)

    # Print the history of the simulation.
    for t, stats in sim.history.items():
        print(f"Time {t}: {stats}")