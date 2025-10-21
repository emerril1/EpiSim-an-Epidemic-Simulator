from Population import Population
from Virus import Virus
from EnumeratedTypes import State
from Intervention import Intervention
from collections import Counter
import json
import csv
import os
import time
import matplotlib.pyplot as plt

class Simulation:
    """Runs the epidemic simulation and tracks population state over time."""

    RESULTS_DIR = "Simidemic/Simulator/results"
    RUN_LOG_FILE = os.path.join(RESULTS_DIR, "simulation_log.csv")

    def __init__(self, config):
        """ Initialize simulation with configuration parameters."""

        # Set up simulation parameters
        self.run_id = self.get_next_run_id()
        self.purpose = config["simulation"]["purpose"]
        self.params_changed = config["simulation"]["params_changed"]
        self.duration = config["simulation"]["duration"]

        # Ensure results directory exists
        os.makedirs(self.RESULTS_DIR, exist_ok = True)

        # Initialize virus and population configurations
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
    
    def get_next_run_id(cls):
        """Read the last run ID from the log and increment it."""

        if not os.path.exists(cls.RUN_LOG_FILE):
            return "001"
        try:
            with open(cls.RUN_LOG_FILE, "r") as file:
                lines = file.readlines()
                if len(lines) <= 1:
                    return "001"
                last_line = lines[-1].strip().split(",")[0]
                next_id = int(last_line) + 1
                return f"{next_id:03d}"
        except Exception:
            return "001"

    def run(self):
        """Run the simulation for the configured duration."""

        start_time = time.time()

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

        runtime = time.time() - start_time

        # Final results
        print(f"\n=== Simulation Complete: {self.virus.name} ===")
        age_counts = Counter([p.age_group for p in self.population.population])
        print(f"Age Group Distribution: {dict(age_counts)}")
        print(f"Comparment Distribution: {self.history[-1]}")
        print(f"Total Runtime: {runtime:.2f} seconds\n")
        
        # Final age breakdown by infection state
        final_age_groups = {g: Counter(p.state for p in self.population.population if p.age_group == g) for g in age_counts.keys()}
        print("\nFinal State by Age Group:")
        for group, states in final_age_groups.items():
            print(f"  {group}: {{S: {states.get(State.SUSCEPTIBLE, 0)}, "
                  f"E: {states.get(State.EXPOSED, 0)}, "
                  f"I: {states.get(State.INFECTED, 0)}, "
                  f"R: {states.get(State.RECOVERED, 0)}}}")
            
        data_filename = self.export_run_data()
        self.log_run(runtime, data_filename)
        self.plot_curve()

    def export_run_data(self):
        """Export SEIR daily data to CSV."""

        data_filename = os.path.join(self.RESULTS_DIR, f"run_{self.run_id}.csv")

        with open(data_filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Day", "Susceptible", "Exposed", "Infected", "Recovered"])
            for day, data in enumerate(self.history, start=1):
                writer.writerow([day, data["S"], data["E"], data["I"], data["R"]])

        print(f"Data exported to {data_filename}")
        return data_filename

    def log_run(self, runtime, data_filename):
        """Log metadata for each run."""

        log_exists = os.path.exists(self.RUN_LOG_FILE)
        with open(self.RUN_LOG_FILE, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if not log_exists:
                writer.writerow(["Run ID", "Purpose", "Parameters Changed", "Duration", "Data File"])
            formatted_time = f"{int(runtime // 60)}m {int(runtime % 60)}s"
            writer.writerow([self.run_id, self.purpose, self.params_changed, formatted_time, os.path.basename(data_filename)])

        print(f"Run logged to {self.RUN_LOG_FILE}")

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

    # Load config
    with open("Simidemic/Simulator/config.json") as f:
        config = json.load(f)
    sim = Simulation(config)

    # Run the simulation
    sim.run()

