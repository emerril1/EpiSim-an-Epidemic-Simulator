from EnumeratedTypes import State
import random

class Intervention:
    """ Manages interventions: vaccination, quarantine, and social distancing."""

    def __init__(self, population, config):
        self.population = population
        self.config = config or {}

        # Flags to ensure one-time interventions
        self.vaccine_applied = False
        self.quarantine_active = False
        self.social_distancing_active = False

    def apply_vaccine(self, day):
        """ Apply vaccination once after the start day."""

        # Extract vaccination configuration safely
        try:
            cfg = self.config.get("intervention", {}).get("vaccination", {})
            if not cfg.get("enabled", False): return
            if day < cfg.get("start_day", 0) or self.vaccine_applied: return

            # Calculate vaccination coverage
            coverage = cfg.get("coverage", 0)
            num = int(coverage * len(self.population.population))
            candidates = random.sample(self.population.population, num)

            # Apply vaccination
            for p in candidates:
                p.vaccinated = True
                p.state = State.RECOVERED

            self.vaccine_applied = True
        except Exception as e:
            print(f"Error: Vaccination failed: {e}")

    def apply_quarantine(self, day):
        """ Quarantine a fraction of infected individuals after the start day."""

        # Extract quarantine configuration safely
        try:
            cfg = self.config.get("intervention", {}).get("quarantine", {})
            if not cfg.get("enabled", False): return
            if day < cfg.get("start_day", 0) or self.quarantine_active: return

            # Calculate quarantine coverage
            coverage = cfg.get("coverage", 0)
            infected = [p for p in self.population.population if p.state == State.INFECTED]
            num = int(coverage * len(infected))

            # Randomly quarantine individuals
            if num > 0:
                isolated = random.sample(infected, num)
                for p in isolated:
                    p.isolated = True 

            self.quarantine_active = True
        except Exception as e:
            print(f"Error: Quarantine failed: {e}")

    def apply_social_distancing(self, day):
        """ Reduce contact rate once after the start day."""

        # Extract social distancing configuration safely
        try:
            cfg = self.config.get("intervention", {}).get("social_distancing", {})
            if not cfg.get("enabled", False): return
            if day < cfg.get("start_day", 0) or self.social_distancing_active: return

            # Apply reduction factor to contact rate of population network
            reduction = cfg.get("reduction_factor", 0)
            self.population.adjust_contact_rate(reduction)
            self.social_distancing_active = True
        except Exception as e:
            print(f"Error: Social distancing failed: {e}")