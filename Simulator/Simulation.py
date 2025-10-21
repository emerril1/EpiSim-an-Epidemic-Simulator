import os, time, json, csv
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt
from copy import deepcopy

from Population import Population
from Virus import Virus
from Intervention import Intervention
from EnumeratedTypes import State

class Simulation:
    """Runs the epidemic simulation and exports data."""

    RESULTS_DIR = "Simidemic/Simulator/results"

    def __init__(self, config):
        self.config = config
        os.makedirs(self.RESULTS_DIR, exist_ok=True)
        self.run_id = self.get_next_run_id()
        self.purpose = config["simulation"]["purpose"]
        self.params_changed = config["simulation"]["params_changed"]
        self.duration = config["simulation"]["duration"]

        # Initialize virus, population, and interventions
        vir_cfg = config["virus"]
        pop_cfg = config["population"]

        self.virus = Virus(
            name=vir_cfg["name"],
            infect_rate=vir_cfg["infect_rate"],
            cure_rate=vir_cfg["cure_rate"],
            infection_time=vir_cfg["infection_time"]
        )

        self.population = Population(
            size=pop_cfg["size"],
            avg_degree=pop_cfg["avg_degree"],
            rewire_prob=pop_cfg["rewire_prob"],
            risk_factors=pop_cfg.get("risk_factors")
        )

        self.intervention = Intervention(self.population, config)

        self.history = []  # Stores SEIR counts per day per age group
        self.event_log = []  # Stores events per individual
        self.runtime_ms = 0.0

    @classmethod
    def get_next_run_id(cls):
        log_file = os.path.join(cls.RESULTS_DIR, "log.csv")
        if not os.path.exists(log_file):
            return "001"
        with open(log_file, "r") as f:
            rows = list(csv.reader(f))
            last_valid = next((r for r in reversed(rows) if r and r[0].isdigit()), None)
            return f"{int(last_valid[0]) + 1:03d}" if last_valid else "001"

    def run(self):
        start_time = time.time()
        # Infect patient zero
        self.population.population[0].state = State.INFECTED

        # Simulation loop
        for day in range(1, self.duration + 1):
            self.intervention.apply_vaccine(day)
            self.intervention.apply_social_distancing(day)
            self.intervention.apply_quarantine(day)

            self.population.update(self.virus, day)
            self.simulate_day(day)

        self.runtime_ms = (time.time() - start_time) * 1000
        self.export_run_data()
        self.log_run()
        self.plot_curve()

    def simulate_day(self, day):
        """Stores snapshot of SEIR counts per age group and records events."""
        age_groups = sorted(set(p.age_group for p in self.population.population))
        day_snapshot = {}
        for group in age_groups:
            members = [p for p in self.population.population if p.age_group == group]
            counts = Counter([p.state for p in members])
            day_snapshot[group] = {
                "S": counts.get(State.SUSCEPTIBLE, 0),
                "E": counts.get(State.EXPOSED, 0),
                "I": counts.get(State.INFECTED, 0),
                "R": counts.get(State.RECOVERED, 0)
            }

        self.history.append(deepcopy(day_snapshot))

        # Record events for this day
        for p in self.population.population:
            if p.just_infected:
                self.event_log.append({"day": day, "PersonID": p.id, "Age": p.age,
                                       "AgeGroup": p.age_group, "Event": "Infected"})
                p.just_infected = False
            if p.just_recovered:
                self.event_log.append({"day": day, "PersonID": p.id, "Age": p.age,
                                       "AgeGroup": p.age_group, "Event": "Recovered"})
                p.just_recovered = False

    def export_run_data(self):
        base = os.path.join(self.RESULTS_DIR, f"run_{self.run_id}")
        timeseries_file = f"{base}_timeseries.csv"
        events_file     = f"{base}_events.csv"
        summary_file    = f"{base}_summary.json"
        config_file     = f"{base}_config.json"
        figure_file     = f"{base}_curve.png"

        # --- Timeseries CSV ---
        with open(timeseries_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Day", "AgeGroup", "Susceptible", "Exposed", "Infected", "Recovered"])
            for day_idx, day_snapshot in enumerate(self.history, start=1):
                for age_group, counts in day_snapshot.items():
                    writer.writerow([day_idx, age_group, counts["S"], counts["E"], counts["I"], counts["R"]])

        # --- Events CSV ---
        with open(events_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Day", "PersonID", "Age", "AgeGroup", "Event"])
            for ev in self.event_log:
                writer.writerow([ev["day"], ev["PersonID"], ev["Age"], ev["AgeGroup"], ev["Event"]])

        # --- Summary JSON ---
        final_counts = self.history[-1] if self.history else {"S":0,"E":0,"I":0,"R":0}
        age_dist = Counter(p.age_group for p in self.population.population)
        summary_data = {
            "RunID": self.run_id,
            "Virus": self.virus.name,
            "PopulationSize": len(self.population.population),
            "DurationDays": self.duration,
            "Runtime_ms": round(self.runtime_ms, 2),
            "Timestamp": datetime.now().isoformat(),
            "FinalState": final_counts,
            "AgeDistribution": dict(age_dist)
        }
        with open(summary_file, "w") as f:
            json.dump(summary_data, f, indent=4)

        # --- Config JSON ---
        with open(config_file, "w") as f:
            json.dump(self.config, f, indent=4)

        print("Data exported to:")
        print(f"   ├─ {summary_file}")
        print(f"   ├─ {timeseries_file}")
        print(f"   ├─ {events_file}")
        print(f"   ├─ {config_file}")
        print(f"   └─ {figure_file}")

        # --- Save figure ---
        self.plot_curve(save_path=figure_file)

    def log_run(self):
        log_file = os.path.join(self.RESULTS_DIR, "log.csv")
        write_header = not os.path.exists(log_file)
        with open(log_file, "a", newline="") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(["RunID", "Virus", "Runtime_ms", "DataFile"])
            writer.writerow([self.run_id, self.virus.name, self.runtime_ms,
                             f"run_{self.run_id}_summary.json"])

    def plot_curve(self, save_path=None):
        if not self.history:
            return
        days = list(range(1, len(self.history)+1))
        S = [sum(day[g]["S"] for g in day) for day in self.history]
        E = [sum(day[g]["E"] for g in day) for day in self.history]
        I = [sum(day[g]["I"] for g in day) for day in self.history]
        R = [sum(day[g]["R"] for g in day) for day in self.history]

        plt.figure(figsize=(10,6))
        plt.plot(days, S, label="Susceptible")
        plt.plot(days, E, label="Exposed")
        plt.plot(days, I, label="Infected")
        plt.plot(days, R, label="Recovered")
        plt.legend()
        plt.xlabel("Day")
        plt.ylabel("Population")
        plt.title(f"Epidemic Simulation: {self.virus.name}")
        plt.grid(True)
        plt.tight_layout()

        # Save the figure
        figure_file = os.path.join(self.RESULTS_DIR, f"run_{self.run_id}_curve.png")
        plt.savefig(figure_file, dpi=300)

if __name__ == "__main__":
    with open("Simidemic/Simulator/config.json") as f:
        config = json.load(f)
    sim = Simulation(config)
    sim.run()