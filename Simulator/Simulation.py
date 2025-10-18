from Population import Population
from Virus import Virus
from Intervention import Intervention 
from EnumeratedTypes import State
import json
import matplotlib.pyplot as plt

class Simulation:
    """ Runs the epidemic simulation and tracks population state over time."""

    def __init__(self, population: Population, virus: Virus, config: dict):
        self.population = population
        self.virus = virus
        self.config = config
        self.intervention = Intervention(population, config)
        self.time = 1
        self.history = {}

    def step(self):
        """ Simulate one day in the epidemic."""

        # Apply interventions
        self.intervention.apply_social_distancing(self.time)
        self.intervention.apply_quarantine(self.time)
        self.intervention.apply_vaccine(self.time)

        # Update population state
        self.population.update(self.virus, self.time)
        self.track_stats()
        self.time += 1

    def run(self, duration):
        """ Run the simulation for the specified duration."""

        # Start simulation loop 
        print(f"Starting simulation for {duration} days...\n")
        for _ in range(duration):
            self.step()
        print("\nSimulation complete.\n")

    def track_stats(self): 
        """ Track and store daily statistics of the population states."""

        # Count individuals in each state
        counts = {
            "S": sum(p.state == State.SUSCEPTIBLE for p in self.population.population),
            "E": sum(p.state == State.EXPOSED for p in self.population.population),
            "I": sum(p.state == State.INFECTED for p in self.population.population),
            "R": sum(p.state == State.RECOVERED for p in self.population.population)
        }

        # Store daily counts
        self.history[self.time] = counts
        print(f"Day {self.time}: {counts}")

    def plot_curve(self):
        """ Plot the epidemic progression over time."""

        # Prepare data for plotting
        days = list(self.history.keys())
        susceptible = [h["S"] for h in self.history.values()]
        exposed = [h["E"] for h in self.history.values()]
        infected = [h["I"] for h in self.history.values()]
        recovered = [h["R"] for h in self.history.values()]

        # Plotting the curves
        plt.figure(figsize = (10, 6))
        plt.plot(days, susceptible, label = "Susceptible", linewidth = 2)
        plt.plot(days, exposed, label = "Exposed", linewidth = 2)
        plt.plot(days, infected, label = "Infected", linewidth = 2)
        plt.plot(days, recovered, label = "Recovered", linewidth = 2)

        # Customize plot
        plt.title("Epidemic Simulation Over Time", fontsize = 14)
        plt.xlabel("Day")
        plt.ylabel("Number of Individuals")
        plt.legend()
        plt.grid(True, linestyle = "--", alpha=0.6)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":

    # Load configuration
    with open("Simidemic/Simulator/config.json") as f:
        config = json.load(f)

    # Initialize components
    pop = Population(
        size = config["population"]["size"],
        avg_degree = config["population"]["avg_degree"],
        rewire_prob = config["population"]["rewire_prob"]
    )
    virus = Virus(
        name = config["virus"]["name"],
        infect_rate = config["virus"]["infect_rate"],
        cure_rate = config["virus"]["cure_rate"],
        infection_time = config["virus"]["infection_time"]
    )

    # Create simulation
    sim = Simulation(pop, virus, config)

    # Infect patient zero
    patient_zero = pop.population[0]
    patient_zero.state = State.INFECTED
    patient_zero.infected_time = 0

    # Run simulation
    sim.run(config["simulation"]["duration"])

    # Plot results
    sim.plot_curve()