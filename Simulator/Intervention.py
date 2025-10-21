from EnumeratedTypes import State
import random

class Intervention:
    """ Class to manage interventions: vaccination, quarantine, and social distancing."""

    def __init__(self, population, config):
        """ Initialize population and intervention configurations."""
        
        self.population = population
        self.config = config

        # Flags to ensure interventions are applied only once if appropriate
        self.vaccine_applied = False
        self.quarantine_active = False
        self.social_distancing_active = False

    def apply_vaccine(self, current_day):
        """ Apply vaccination to a portion of the population."""

        # Check if vaccination is enabled and not yet applied
        cfg = self.config.get("intervention", {}).get("vaccination", {})
        if not cfg.get("enabled", False):
            return

        start_day = cfg.get("start_day")
        if current_day < start_day or self.vaccine_applied:
            return
        
        # Determine number to vaccinate
        coverage = cfg.get("coverage")
        num_to_vaccinate = int(coverage * len(self.population.population))
        candidates = random.sample(self.population.population, num_to_vaccinate)

        # Vaccinate selected individuals
        for p in candidates:
            p.vaccinated = True

        # Mark vaccination as applied
        self.vaccine_applied = True
        print(f"[Day {current_day}] Vaccine applied to {num_to_vaccinate} individuals ")

    def apply_quarantine(self, current_day):
        """ Isolate a portion of infected individuals."""

        # Check if quarantine is enabled and not yet active
        cfg = self.config.get("intervention", {}).get("quarantine", {})
        if not cfg.get("enabled", False):
            return

        start_day = cfg.get("start_day")
        if current_day < start_day or self.quarantine_active:
            return

        # Apply quarantine to a portion of infected individuals
        coverage = cfg.get("coverage", 0)
        infected = [p for p in self.population.population if p.state == State.INFECTED]
        num_to_quarantine = int(coverage * len(infected))

        # Quarantine selected individuals
        if num_to_quarantine > 0:
            isolated = random.sample(infected, num_to_quarantine)
            for p in isolated:
                p.isolated = True

        # Mark quarantine as applied
        self.quarantine_active = True
        print(f"[Day {current_day}] Quarantine started — isolated {num_to_quarantine} infected individuals.")
       
    def apply_social_distancing(self, current_day):
        """ Reduce contact rates in the population."""

        # Check if social distancing is enabled and not yet active
        cfg = self.config.get("intervention", {}).get("social_distancing", {})
        if not cfg.get("enabled", False):
            return

        start_day = cfg.get("start_day")
        if current_day < start_day or self.social_distancing_active:
            return

        # Apply contact rate reduction
        reduction = cfg.get("reduction_factor")
        self.population.adjust_contact_rate(reduction)

        # Mark social distancing as applied
        self.social_distancing_active = True
        print(f"[Day {current_day}] Social distancing applied - contact rate reduced by {reduction*100:.0f}%")
