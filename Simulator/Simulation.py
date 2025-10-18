from Population import Population
from Virus import Virus
from Intervention import Intervention 
from EnumeratedTypes import State
import random
import json
import matplotlib.pyplot as plt

class Simulation:
    ''' Main simulation class that runs the epidemic simulation.
        Tracks the state of the population over time and applies virus dynamics.'''

    # Initialize simulation with population, virus, and configuration
    def __init__(self, population, virus, config):
        self.population = population
        self.virus = virus
        self.config = config
        self.time = 1
        self.history = {}

        # Initialize interventions handler
        self.interventions = Intervention(population, config)
        self.interventions.vaccinate()

    def step(self):
        ''' Perform a single time step in the simulation.
            Process infections, recoveries, and apply interventions.'''

        # Determine contact factor based on interventions. Can combine effects.
        sd_factor = self.interventions.social_distancing(self.time)
        q_factor = self.interventions.quarantine(self.time)
        contact_factor = sd_factor * q_factor

        # Process infections and recoveries
        new_exposures = []
        new_infections = []

        # Iterate over all individuals in the population
        for person in self.population.population:

            # Infectious people spread infection
            if person.state == State.INFECTED:

                # Get contacts adjusted by contact factor
                contacts = self.population.get_contacts(person)
                num_contacts = int(len(contacts) * contact_factor)
                reduced_contacts = random.sample(contacts, num_contacts) if num_contacts > 0 else []

                # Attempt to infect contacts
                for contact in reduced_contacts:
                    if contact.state == State.SUSCEPTIBLE:
                        infect_chance = self.virus.infect_rate
                        if getattr(contact, "vaccinated", False):
                            infect_chance *= (1 - contact.vaccine_effectiveness)
                        if random.random() < infect_chance:
                            new_exposures.append(contact)

                # Cure infected individuals
                if random.random() < self.virus.cure_rate:
                    person.cure()

        # Process exposed individuals becoming infected
        for person in self.population.population:
            if person.state == State.EXPOSED and self.time - person.exposed_time >= self.virus.infection_time:
                new_infections.append(person)

        # Apply new state transitions
        for p in new_exposures:
            p.expose(self.time)
        for p in new_infections:
            p.infect(self.time)

        # Track statistics
        self.track_stats()
        self.time += 1

    def run(self, num_of_steps: int):
        ''' Run the simulation for a specified number of steps.'''

        print(f"Simulation running for {num_of_steps} days...")
        for _ in range(num_of_steps):
            self.step()

    def track_stats(self):
        ''' Track the number of susceptible, infected, and recovered individuals.'''
        
        # Count individuals in each state and store in history
        counts = {
            "S": sum(1 for p in self.population.population if p.state == State.SUSCEPTIBLE),
            "E": sum(1 for p in self.population.population if p.state == State.EXPOSED),
            "I": sum(1 for p in self.population.population if p.state == State.INFECTED),
            "R": sum(1 for p in self.population.population if p.state == State.RECOVERED)
        }
        self.history[self.time] = counts

    def plot_curve(self):
        ''' Plot the infection curve over time.'''

        # Prepare data for plotting
        days = list(sim.history.keys())

        # Extract state counts
        susceptible = [h.get("S", 0) for h in sim.history.values()]
        exposed     = [h.get("E", 0) for h in sim.history.values()] if "E" in next(iter(sim.history.values()), {}) else None
        infected    = [h.get("I", 0) for h in sim.history.values()]
        recovered   = [h.get("R", 0) for h in sim.history.values()]

        # Plotting
        plt.figure(figsize=(10,6))
        plt.plot(days, susceptible, label="Susceptible", linewidth=2)
        if exposed:
            plt.plot(days, exposed, label="Exposed", linewidth=2)
        plt.plot(days, infected, label="Infected", linewidth=2)
        plt.plot(days, recovered, label="Recovered", linewidth=2)

        # Plot formatting
        plt.title("Epidemic Simulation Over Time", fontsize=14)
        plt.xlabel("Day")
        plt.ylabel("Number of Individuals")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    ''' Example of running a simulation with configuration from a JSON file.'''

    # Load configuration from JSON file
    with open("Simidemic/Simulator/config.json", "r") as f:
        config = json.load(f)

    pop_info = config["population"]
    virus_info = config["virus"]
    sim_info = config["simulation"]
    int_info = config["intervention"]

    # Initialize population, virus, and simulation
    pop = Population(
        size = pop_info["size"],
        avg_degree = pop_info["avg_degree"],
        rewire_prob = pop_info["rewire_prob"]
    )
    virus = Virus(
        name = virus_info["name"],
        infect_rate = virus_info["infect_rate"],
        cure_rate = virus_info["cure_rate"],
        infection_time = virus_info["infection_time"]
    )
    sim = Simulation(pop, virus, config)

    # Initialize patient zero
    for _ in range(sim_info["initial_infected"]):
        patient_zero = random.choice(pop.population)
        patient_zero.infect(time = 0)

    # Run the simulation
    sim.run(sim_info["steps"])

    # Print results
    for t, stats in sim.history.items():
        print(f"Day {t}: {stats}")
    print("Simulation complete.")

    # Plot infection curve
    sim.plot_curve()


