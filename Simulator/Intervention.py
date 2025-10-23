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
            if day < cfg.get("start_day", 20) or self.vaccine_applied: return

            # Calculate vaccination coverage
            coverage = cfg.get("coverage", 0.5)
            num = int(coverage * len(self.population.population))
            candidates = random.sample(self.population.population, num)

            # Apply vaccination
            for p in candidates:
                p.vaccinated = True
                p.state = State.RECOVERED

            # Save vaccination status
            self.vaccine_applied = True
        except Exception as e:
            print(f"Error: Vaccination failed: {e}")

    def apply_quarantine(self, day):
        """ Isolate a portion of infected individuals daily after start_day."""

        # Extract quarantine configuration safely 
        try:
            cfg = self.config.get("intervention", {}).get("quarantine", {})
            if not cfg.get("enabled", False): return
            if day < cfg.get("start_day", 20) or self.quarantine_active: return

            # Calculate quarantine coverage
            coverage = cfg.get("coverage", 0.5)
            infected = [p for p in self.population.population if p.state == State.INFECTED and not p.isolated]
            num_to_quarantine = int(coverage * len(infected))

            # Randomly select infected individuals to quarantine
            if num_to_quarantine > 0:
                isolated = random.sample(infected, num_to_quarantine)
                for p in isolated:
                    p.isolated = True
            
            # Save quarantine status
            self.quarantine_active = True
        except Exception as e:
            print(f"Error: Quarantine failed: {e}")

    def apply_social_distancing(self, day):
        """ Reduce contact rate once after the start day."""

        # Extract social distancing configuration safely
        try:
            cfg = self.config.get("intervention", {}).get("social_distancing", {})
            if not cfg.get("enabled", False): return
            if day < cfg.get("start_day", 20) or self.social_distancing_active: return

            # Apply reduction factor to contact rate of population network
            reduction = cfg.get("reduction_factor", 0.25)
            self.population.adjust_contact_rate(reduction)

            # Save social distancing status
            self.social_distancing_active = True
        except Exception as e:
            print(f"Error: Social distancing failed: {e}")