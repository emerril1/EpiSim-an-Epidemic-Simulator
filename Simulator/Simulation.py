from Population import Population
from Virus import Virus
from EnumeratedTypes import State
from Intervention import Intervention
from collections import Counter
import json
import csv
import os
import time
from datetime import datetime
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

        self.config = config

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

        self.event_log = []
    
    @classmethod
    def get_next_run_id(cls):
        """Return the next run id string '001', '002', ... by reading RUN_LOG_FILE."""
        # Ensure results dir exists
        os.makedirs(cls.RESULTS_DIR, exist_ok=True)

        # If no log file, start at 001
        if not os.path.exists(cls.RUN_LOG_FILE):
            return "001"

        try:
            with open(cls.RUN_LOG_FILE, "r", newline="") as f:
                reader = csv.reader(f)
                rows = list(reader)

                # If file only has header or is empty, start at 001
                if len(rows) <= 1:
                    return "001"

                # Find the last row that appears to have a numeric Run ID in column 0
                for row in reversed(rows):
                    if row and row[0].strip().isdigit():
                        last_id = int(row[0].strip())
                        return f"{last_id + 1:03d}"

                # Fallback
                return "001"
        except Exception as e:
            print(f"[Warning] get_next_run_id failed: {e}")
            return "001"
        
    def run(self):
        """Run the simulation for the configured duration."""

        start_time = time.time()

        # Infect patient zero
        initial_infected = self.population.population[0]
        initial_infected.state = State.INFECTED

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

            # Save daily summary (used by plot and export)
            self.history.append(ordered)

            # Count infected by age group
            infected_by_age = Counter([
                p.age_group for p in self.population.population
                if p.state == State.INFECTED
            ])

            print(f"{self.virus.name} — Day {day}: {ordered} | Infected by Age: {dict(infected_by_age)}")

        runtime_ms = (time.time() - start_time) * 1000

        # Final results
        print(f"\n=== Simulation Complete: {self.virus.name} ===")
        age_counts = Counter([p.age_group for p in self.population.population])
        print(f"Age Group Distribution: {dict(age_counts)}")
        print(f"Compartment Distribution: {self.history[-1]}")
        print(f"Total Runtime: {runtime_ms:.2f} milliseconds\n")

        # Final age breakdown by infection state
        final_age_groups = {g: Counter(p.state for p in self.population.population if p.age_group == g)
                            for g in age_counts.keys()}
        print("Final State by Age Group:")
        for group, states in final_age_groups.items():
            print(f"  {group}: {{S: {states.get(State.SUSCEPTIBLE, 0)}, "
                f"E: {states.get(State.EXPOSED, 0)}, "
                f"I: {states.get(State.INFECTED, 0)}, "
                f"R: {states.get(State.RECOVERED, 0)}}}")

        # Exports
        data_filename = self.export_run_data()
        self.log_run(runtime_ms, data_filename)
        self.plot_curve()

    def export_run_data(self):
        """Export SEIR daily data by age group and individual events."""

        base_filename = os.path.join(self.RESULTS_DIR, f"run_{self.run_id}")
        summary_file = f"{base_filename}_summary.csv"
        timeseries_file = f"{base_filename}_timeseries.csv"
        events_file = f"{base_filename}_events.csv"

        # ====== TIME SERIES EXPORT ======
        age_groups = sorted(set(p.age_group for p in self.population.population))
        with open(timeseries_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            header = ["Day", "AgeGroup", "Susceptible", "Exposed", "Infected", "Recovered"]
            writer.writerow(header)

            for day in range(1, len(self.history) + 1):
                # reconstruct daily SEIR counts from population snapshot
                for age_group in age_groups:
                    members = [p for p in self.population.population if p.age_group == age_group]
                    counts = Counter([p.state for p in members])
                    writer.writerow([
                        day,
                        age_group,
                        counts.get(State.SUSCEPTIBLE, 0),
                        counts.get(State.EXPOSED, 0),
                        counts.get(State.INFECTED, 0),
                        counts.get(State.RECOVERED, 0)
                    ])

        # ====== EVENTS EXPORT ======
        with open(events_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["PersonID", "AgeGroup", "Event", "Day", "StateBefore", "StateAfter"])

            for p in self.population.population:
                if p.exposed_time is not None:
                    writer.writerow([p.id, p.age_group, "Exposed", p.exposed_time, "SUSCEPTIBLE", "EXPOSED"])
                if p.infected_time is not None:
                    writer.writerow([p.id, p.age_group, "Infected", p.infected_time, "EXPOSED", "INFECTED"])
                if p.state == State.RECOVERED:
                    writer.writerow([p.id, p.age_group, "Recovered", "N/A", "INFECTED", "RECOVERED"])

        # ====== SUMMARY EXPORT ======
        with open(summary_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["RunID", "Virus", "PopulationSize", "DurationDays"])
            writer.writerow([self.run_id, self.virus.name, len(self.population.population), self.duration])

        print(f"\nData exported to:\n"
            f"   ├─ {summary_file}\n"
            f"   ├─ {timeseries_file}\n"
            f"   └─ {events_file}")

        return summary_file

    def log_run(self, runtime_ms, data_filename):
        """Log metadata for this run into the single RUN_LOG_FILE (results/simulation_log.csv)."""
        # Ensure folder exists
        os.makedirs(self.RESULTS_DIR, exist_ok=True)

        write_header = not os.path.exists(self.RUN_LOG_FILE)

        # Use self.run_id (already allocated)
        record = {
            "Run ID": self.run_id,
            "Purpose": self.purpose,
            "Parameters Changed": self.params_changed,
            "Duration (ms)": f"{runtime_ms:.2f}",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Data File": os.path.basename(data_filename)
        }

        # Append to the consistent RUN_LOG_FILE
        with open(self.RUN_LOG_FILE, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(record.keys()))
            if write_header:
                writer.writeheader()
            writer.writerow(record)

        print(f"Logged Run {self.run_id} → {self.RUN_LOG_FILE}")

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

