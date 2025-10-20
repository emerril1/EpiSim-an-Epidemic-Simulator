from Population import Population
from Virus import Virus
from EnumeratedTypes import State
from Intervention import Intervention
from collections import Counter
import json
import matplotlib.pyplot as plt

class Simulation:
    """Runs the epidemic simulation and tracks population state over time."""

    def __init__(self, config):
        self.duration = config["simulation"]["duration"]
        vir_cofg = config["virus"]
        pop_cfg = config["population"]

        # Initialize virus
        self.virus = Virus( 
           name = vir_cofg["name"], 
           infect_rate = vir_cofg["infect_rate"], 
           cure_rate = vir_cofg["cure_rate"], 
           infection_time = vir_cofg["infection_time"] 
        )

        # Initialize population
        self.population = Population(
            size = pop_cfg["size"],
            avg_degree = pop_cfg["avg_degree"],
            rewire_prob = pop_cfg["rewire_prob"],
            risk_factors = pop_cfg.get("risk_factors", None)
        )

        # Initialize interventions
        self.intervention = Intervention(self.population, config)
        self.history = []

    def run(self):
        """Run the simulation for the configured duration."""

        # Infect patient zero
        initial_infected = self.population.population[0]
        initial_infected.state = State.INFECTED

        # Start simulation
        print(f"\n=== Starting Simulation: {self.virus.name} ===\n")
        for day in range(1, self.duration + 1):

            # Apply interventions (based on config)
            self.intervention.apply_vaccine(day)
            self.intervention.apply_social_distancing(day)
            self.intervention.apply_quarantine(day)

            # Update infection states
            self.population.update(self.virus, day)

            # Count SEIR states
            counts = Counter([p.state for p in self.population.population])
            ordered = {
                "S": counts.get(State.SUSCEPTIBLE, 0),
                "E": counts.get(State.EXPOSED, 0),
                "I": counts.get(State.INFECTED, 0),
                "R": counts.get(State.RECOVERED, 0)
            }

            # Count infected by age group
            infected_by_age = Counter([
                p.age_group for p in self.population.population
                if p.state == State.INFECTED
            ])

            # Store and print
            self.history.append(ordered)
            print(f"{self.virus.name} — Day {day}: {ordered} | Infected by Age: {dict(infected_by_age)}")

        # Final results
        print(f"\n=== Simulation Complete: {self.virus.name} ===")
        age_counts = Counter([p.age_group for p in self.population.population])
        print(f"Age Group Distribution: {dict(age_counts)}")
        print(f"Comparment Distribution: {self.history[-1]}")
        
        # Final age breakdown by infection state
        final_age_groups = {g: Counter(p.state for p in self.population.population if p.age_group == g) for g in age_counts.keys()}
        print("\nFinal State by Age Group:")
        for group, states in final_age_groups.items():
            print(f"  {group}: {{S: {states.get(State.SUSCEPTIBLE, 0)}, "
                  f"E: {states.get(State.EXPOSED, 0)}, "
                  f"I: {states.get(State.INFECTED, 0)}, "
                  f"R: {states.get(State.RECOVERED, 0)}}}")
            
        # Plot the epidemic curve
        self.plot_curve()

    def plot_curve(self):
        """Plot the epidemic progression over time."""

        # Prepare data
        days = list(range(1, len(self.history) + 1))
        S = [day["S"] for day in self.history]
        E = [day["E"] for day in self.history]
        I = [day["I"] for day in self.history]
        R = [day["R"] for day in self.history]

        # Plotting
        plt.figure(figsize = (10, 6))
        plt.plot(days, S, label = "Susceptible")
        plt.plot(days, E, label = "Exposed")
        plt.plot(days, I, label = "Infected")
        plt.plot(days, R, label = "Recovered")

        # Finalize plot
        plt.title(f"Epidemic Simulation: {self.virus.name}")
        plt.xlabel("Day")
        plt.ylabel("Number of People")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":

    # Load configuration
    with open("Simidemic/Simulator/config.json") as f:
        config = json.load(f)

    # Create and run simulation
    sim = Simulation(config)
    sim.run()