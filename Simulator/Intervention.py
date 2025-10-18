from EnumeratedTypes import State
import random

class Intervention:
    """Class to manage interventions: vaccination, quarantine, and social distancing."""

    def __init__(self, population, config):
        self.population = population
        self.config = config

        # Flags to ensure interventions are applied only once if appropriate
        self.vaccine_applied = False
        self.quarantine_active = False
        self.social_distancing_active = False

    def apply_vaccine(self, current_day):
        cfg = self.config.get("intervention", {}).get("vaccination", {})
        if not cfg.get("enabled", False):
            return

        start_day = cfg.get("start_day")
        if current_day < start_day or self.vaccine_applied:
            return

        coverage = cfg.get("coverage")
        num_to_vaccinate = int(coverage * len(self.population.population))
        candidates = random.sample(self.population.population, num_to_vaccinate)

        for p in candidates:
            p.vaccinated = True

        self.vaccine_applied = True
        print(f"[Day {current_day}] Vaccine applied to {num_to_vaccinate} individuals ")

    def apply_quarantine(self, current_day):
        cfg = self.config.get("intervention", {}).get("quarantine", {})
        if not cfg.get("enabled", False):
            return

        start_day = cfg.get("start_day")
        if current_day < start_day or self.quarantine_active:
            return

        coverage = cfg.get("coverage", 0)
        infected = [p for p in self.population.population if p.state == State.INFECTED]
        num_to_quarantine = int(coverage * len(infected))
        if num_to_quarantine > 0:
            isolated = random.sample(infected, num_to_quarantine)
            for p in isolated:
                p.isolated = True
                
        self.quarantine_active = True
        print(f"[Day {current_day}] Quarantine started — isolated {num_to_quarantine} infected individuals.")

       

    def apply_social_distancing(self, current_day):
        cfg = self.config.get("intervention", {}).get("social_distancing", {})
        if not cfg.get("enabled", False):
            return

        start_day = cfg.get("start_day")
        if current_day < start_day or self.social_distancing_active:
            return

        reduction = cfg.get("reduction_factor")
        self.population.adjust_contact_rate(reduction)

        self.social_distancing_active = True
        print(f"[Day {current_day}] Social distancing applied - contact rate reduced by {reduction*100:.0f}%")
