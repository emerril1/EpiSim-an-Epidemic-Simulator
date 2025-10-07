from Population import Population
from Virus import Virus
from Intervention import Intervention 
from EnumeratedTypes import State
from EnumeratedTypes import InterventionType
import random
import json

class Simulation:
    ''' Main simulation class that runs the epidemic simulation.
        Tracks the state of the population over time and applies virus dynamics.'''

    def __init__(self, population: Population, virus: Virus):
        ''' Initialize with a population and a virus.'''
        
        self.population = population
        self.virus = virus
        self.time = 1
        self.history = {}
        
    def step(self):
        ''' Perform a single time step in the simulation. Performs specific operations based on state of individual (e.g. cure, infect)'''
        
        new_exposures = []
        new_infections = []
        new_recoveries = []

        for person in self.population.population:
            if person.state == State.INFECTED:
                for contact in self.population.get_contacts(person):
                    if contact.state == State.SUSCEPTIBLE and random.random() < self.virus.infect_rate:
                        new_exposures.append(contact)
                if random.random() < self.virus.cure_rate:
                    new_recoveries.append(person)

            elif person.state == State.EXPOSED:
                if self.time - person.exposed_time >= self.virus.infection_time:
                    new_infections.append(person)

        for p in new_exposures:
            p.expose(self.time)
        for p in new_infections:
            p.infect(self.time)
        for p in new_recoveries:
            p.cure()

        self.track_stats()
        self.time += 1

    def run(self, num_of_steps: int):
        ''' Run the simulation for a specified number of steps.'''
        
        for _ in range (num_of_steps):
            self.step()

    def track_stats(self):
        ''' Track the number of susceptible, infected, and recovered individuals.'''
        
        counts = {
            "S": sum(1 for p in self.population.population if p.state == State.SUSCEPTIBLE),
            "E": sum(1 for p in self.population.population if p.state == State.EXPOSED),
            "I": sum(1 for p in self.population.population if p.state == State.INFECTED),
            "R": sum(1 for p in self.population.population if p.state == State.RECOVERED)
        }
        self.history[self.time] = counts

if __name__ == "__main__":
    ''' Example of running a simulation with configuration from a JSON file.'''

    with open("Simulator/config.json", "r") as f:
        config = json.load(f)

    pop_size = config["population"]["size"]
    virus_info = config["virus"]
    sim_info = config["simulation"]

    pop = Population(size = pop_size)
    virus = Virus(
        name = virus_info["name"],
        infect_rate = virus_info["infect_rate"],
        cure_rate = virus_info["cure_rate"],
        infection_time = virus_info["infection_time"]
    )
    sim = Simulation(pop, virus)

    # Initialize patient zero
    for _ in range(sim_info["initial_infected"]):
        patient_zero = random.choice(pop.population)
        patient_zero.infect(time = 0)

    print("Starting simulation...")
    sim.run(sim_info["steps"])

    # Print results
    for t, stats in sim.history.items():
        print(f"Day {t}: {stats}")