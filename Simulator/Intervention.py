from EnumeratedTypes import State
import random

class Interventions:
    ''' Class to manage various interventions in the simulation. '''

    def __init__(self, population, config):
        self.population = population
        self.config = config
        self.active_quarantine = False
        self.quarantine_timer = 0

    def vaccinate(self):
        ''' Function to vaccinate a portion of the population at the start of the simulation.'''

        # Setup vaccination parameters
        vaccine_cfg = self.config["intervention"].get("vaccine", {})
        if not vaccine_cfg.get("enabled", False):
            return

        # Vaccinate a portion of the population
        coverage = vaccine_cfg.get("coverage", 0)
        effectiveness = vaccine_cfg.get("effectiveness", 1.0)
        num_vaccinated = int(len(self.population.population) * coverage)

        # Randomly select individuals to vaccinate
        vaccinated_people = random.sample(self.population.population, num_vaccinated)
        for person in vaccinated_people:
            person.vaccinated = True
            person.vaccine_effectiveness = effectiveness

        # Log vaccination event
        print(f"[Vaccine] {num_vaccinated} people vaccinated ({effectiveness*100:.0f}% effective).")

    def quarantine(self, time):
        ''' Function to manage quarantine measures based on infection levels.'''

        # Setup quarantine parameters
        quarantine_cfg = self.config["intervention"].get("quarantine", {})
        if not quarantine_cfg.get("enabled", False):
            return 1.0

        # Calculate current infected fraction
        infected_fraction = sum(1 for p in self.population.population if p.state == State.INFECTED) / len(self.population.population)

        # Trigger quarantine
        if (not self.active_quarantine and infected_fraction >= quarantine_cfg.get("threshold", 1.1)):
            self.active_quarantine = True
            self.quarantine_timer = quarantine_cfg.get("duration", 0)
            print(f"[Quarantine] Triggered on day {time} (infected={infected_fraction:.2f}).")

        # Maintain or end quarantine
        if self.active_quarantine:
            effectiveness = quarantine_cfg.get("effectiveness", 0.0)
            self.quarantine_timer -= 1
            if self.quarantine_timer <= 0:
                self.active_quarantine = False
                print(f"[Quarantine] Lifted on day {time}.")
            return 1 - effectiveness
        return 1.0

    def social_distancing(self, time):
        ''' Function to adjust contact factor based on social distancing measures.'''

        # Setup social distancing parameters
        sd_cfg = self.config["intervention"].get("social_distancing", {})
        if not sd_cfg.get("enabled", False):
            return 1.0

        # Determine if within social distancing period
        start_day = sd_cfg.get("start_day", 0)
        duration = sd_cfg.get("duration", 0)
        reduction = sd_cfg.get("contact_reduction", 0.0)

        if start_day <= time < start_day + duration:
            return 1 - reduction
        return 1.0