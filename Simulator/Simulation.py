import os, time, json, csv
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt

from Population import Population
from Virus import Virus
from Intervention import Intervention
from EnumeratedTypes import State

class Simulation:
    """ Run an epidemic simulation, record results, and export all data."""

    RESULTS_DIR = "Simidemic/Simulator/results"

    def __init__(self, config):
        """ Initialize simulation parameters and configuration data"""

        self.config = config
        os.makedirs(self.RESULTS_DIR, exist_ok = True)

        # Initialize simulation metadata
        sim_cfg = config["simulation"]
        self.run_id = self.get_next_run_id()
        self.duration = sim_cfg["duration"]
        self.purpose = sim_cfg["purpose"]
        self.params_changed = sim_cfg["params_changed"]

        # Initializes Virus config parameters
        vir_cfg = config["virus"]
        self.virus = Virus(
            name = vir_cfg["name"],
            infect_rate = vir_cfg["infect_rate"],
            cure_rate = vir_cfg["cure_rate"],
            infection_time = vir_cfg["infection_time"]
        )

        # Initializes Population config parameters
        pop_cfg = config["population"]
        self.population = Population(
            size = pop_cfg["size"],
            avg_degree = pop_cfg["avg_degree"],
            rewire_prob = pop_cfg["rewire_prob"],
            risk_factors = pop_cfg.get("risk_factors")
        )

        # Initializes Intervention config parameters
        self.intervention = Intervention(self.population, config)

        # Tracks statisitics for final exported logs
        self.history = []      
        self.event_log = []   
        self.runtime_ms = 0.0  

    @classmethod
    def get_next_run_id(cls):
        """ Get the next sequential run ID."""

        os.makedirs(cls.RESULTS_DIR, exist_ok = True)
        log_path = os.path.join(cls.RESULTS_DIR, "log.csv")

        if not os.path.exists(log_path):
            return "001"

        with open(log_path, "r", newline = "") as file:
            rows = list(csv.reader(file))
            last_valid = next((r for r in reversed(rows) if r and r[0].isdigit()), None)
            if not last_valid:
                return "001"
            return f"{int(last_valid[0]) + 1:03d}"

    def run(self):
        """ Main simulation loop."""

        start_time = time.time()

        # Infect patient zero
        self.population.population[0].state = State.INFECTED

        for day in range(1, self.duration + 1):
            self.simulate_day(day)

        self.runtime_ms = (time.time() - start_time) * 1000

        # Export and log
        summary_file = self.export_run_data()
        self.log_run(summary_file)
        self.plot_curve(save_path = f"{self.RESULTS_DIR}/run_{self.run_id}_curve.png")

    def simulate_day(self, day):
        """ Simulate one day of infection spread and interventions."""

        prev_states = [p.state for p in self.population.population]

        # Apply interventions
        self.intervention.apply_vaccine(day)
        self.intervention.apply_social_distancing(day)
        self.intervention.apply_quarantine(day)

        # Update population
        self.population.update(self.virus, day)

        # Record counts
        counts = Counter(p.state for p in self.population.population)
        ordered = {
            "S": counts.get(State.SUSCEPTIBLE, 0),
            "E": counts.get(State.EXPOSED, 0),
            "I": counts.get(State.INFECTED, 0),
            "R": counts.get(State.RECOVERED, 0)
        }
        self.history.append(ordered)

        # Track state transitions
        for idx, person in enumerate(self.population.population):
            old, new = prev_states[idx], person.state
            if old != new:
                self.event_log.append({
                    "day": day,
                    "PersonID": getattr(person, "id", idx),
                    "Age": getattr(person, "age", "Unknown"),
                    "AgeGroup": getattr(person, "age_group", "Unknown"),
                    "Event": f"{old.name} → {new.name}"
                })

    def export_run_data(self):
        """ Export simulation results to CSV/JSON."""

        base = os.path.join(self.RESULTS_DIR, f"run_{self.run_id}")
        files = {
            "timeseries": f"{base}_timeseries.csv",
            "events": f"{base}_events.csv",
            "summary": f"{base}_summary.json",
            "config": f"{base}_config.json",
            "figure": f"{base}_curve.png"
        }

        # --- Timeseries ---
        with open(files["timeseries"], "w", newline = "") as f:
            writer = csv.writer(f)
            writer.writerow(["Day", "Susceptible", "Exposed", "Infected", "Recovered"])
            for day, counts in enumerate(self.history, 1):
                writer.writerow([day, counts["S"], counts["E"], counts["I"], counts["R"]])

        # --- Events ---
        with open(files["events"], "w", newline = "", encoding = "utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Day", "PersonID", "Age", "AgeGroup", "Event"])
            for e in self.event_log:
                writer.writerow([
                    e.get("day", ""), e.get("PersonID", ""),
                    e.get("Age", ""), e.get("AgeGroup", ""), e.get("Event", "")
                ])

        # --- Summary ---
        final_counts = self.history[-1] if self.history else {"S": 0, "E": 0, "I": 0, "R": 0}
        total_counts = {k: sum(day[k] for day in self.history) for k in final_counts}
        total_infections = total_counts["I"]
        throughput = total_infections / self.runtime_ms if self.runtime_ms > 0 else 0
        age_dist = Counter(p.age_group for p in self.population.population)

        summary = {
            "RunID": self.run_id,
            "Purpose": self.purpose,
            "ParametersChanged": self.params_changed,
            "Virus": self.virus.name,
            "PopulationSize": len(self.population.population),
            "DurationDays": self.duration,
            "Runtime_ms": round(self.runtime_ms, 4),
            "Timestamp": datetime.now().isoformat(),
            "FinalState": final_counts,
            "AgeDistribution": dict(age_dist),
            "TotalCounts": total_counts,
            "Throughput": round(throughput, 4)
        }

        with open(files["summary"], "w") as f:
            json.dump(summary, f, indent=4)

        # --- Config ---
        with open(files["config"], "w") as f:
            json.dump(self.config, f, indent=4)

        print("Data exported:")
        for label, path in files.items():
            print(f"   ├─ {path}")

        return files["summary"], files["config"]

    def log_run(self, summary_file):
        """ Record this run in a persistent CSV log."""

        log_path = os.path.join(self.RESULTS_DIR, "log.csv")
        new_file = not os.path.exists(log_path)

        with open(log_path, "a", newline = "") as f:
            writer = csv.writer(f)
            if new_file:
                writer.writerow(["RunID", "Purpose", "ParametersChanged", "Runtime (ms)", "SummaryFile"])
            writer.writerow([self.run_id, self.purpose, self.params_changed, round(self.runtime_ms, 4), summary_file])

        print(f"Run logged → {log_path}")

    def plot_curve(self, save_path = None):
        """ Plot and save epidemic progression curves."""

        if not self.history:
            print("[WARN] No data to plot.")
            return

        days = range(1, len(self.history) + 1)
        S = [h["S"] for h in self.history]
        E = [h["E"] for h in self.history]
        I = [h["I"] for h in self.history]
        R = [h["R"] for h in self.history]

        plt.figure(figsize = (10, 6))
        plt.plot(days, S, label = "Susceptible")
        plt.plot(days, E, label = "Exposed")
        plt.plot(days, I, label = "Infected")
        plt.plot(days, R, label = "Recovered")
        plt.title(f"Epidemic Simulation: {self.virus.name}")
        plt.xlabel("Day")
        plt.ylabel("Population")
        plt.legend()
        plt.grid(True)

        if save_path:
            plt.savefig(save_path)
            print(f"Plot saved → {save_path}")
        plt.close()

if __name__ == "__main__":

    # Loads config file and calls the simulation run function
    with open("Simidemic/Simulator/config.json") as f:
        config = json.load(f)
    sim = Simulation(config)
    sim.run()