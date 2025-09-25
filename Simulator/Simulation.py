from Population import Population
from Virus import Virus
from EnumeratedTypes import State
import networkx as nx
import random

class Simulation:
    def __init__(self, population: Population, virus: Virus):
        self.population = population
        self.virus = virus
        self.time = 0
        self.history = {}
    
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

    def run(self, num_of_steps: int):
        for _ in range (num_of_steps):
            self.step()
    
    def track_stats(self):
        counts = {
            "S": sum(1 for p in self.population.population if p.state == State.SUSCEPTIBLE),
            "I": sum(1 for p in self.population.population if p.state == State.INFECTED),
            "R": sum(1 for p in self.population.population if p.state == State.RECOVERED)
        }
        self.history[self.time] = counts

if __name__ == "__main__":
    pop = Population(size = 50)
    virus = Virus("Virus", infect_rate = 0.2, cure_rate = 0.05)
    sim = Simulation(pop, virus)

    patient_zero = random.choice(pop.population)
    patient_zero.infect(time = 0)

    print("Patient zero:", patient_zero.id, "neighbors:", [p.id for p in pop.get_contacts(patient_zero)])

    sim.run(20)

    for t, stats in sim.history.items():
        print(f"Time {t}: {stats}")