from EnumeratedTypes import State
import random

class Person:
    """ Represents one individual in the population and their health state."""

    # Shared across all Person instances
    _global_id_counter = 0

    def __init__(self):
        """ Initialize a person with a unique global ID and default to susceptible."""

        # ID counters for counting each person in simulation
        self.id = Person._global_id_counter
        Person._global_id_counter += 1

        # Individual person statistics
        self.state = State.SUSCEPTIBLE
        self.exposed_time = None
        self.infected_time = None
        self.vaccinated = False
        self.vaccine_effectiveness = 0.0
        self.isolated = False
        self.age = random.randint(0, 100)
        self.age_group = self.assign_age_group()

        # Tracking attributes for simulation events
        self.days_exposed = 0
        self.days_infected = 0
        self.just_infected = False
        self.just_recovered = False

    def assign_age_group(self):
        """ Assign a person to an age group based on age."""
        
        if self.age < 18:
            return "child"
        elif self.age < 65:
            return "adult"
        else:
            return "senior"

    def expose(self, time):
        """ Expose a susceptible person to the virus (S → E)."""

        # Only expose if susceptible
        if self.state == State.SUSCEPTIBLE:
            self.state = State.EXPOSED
            self.exposed_time = time
            self.days_exposed = 0

    def infect(self, time):
        """ Infect an exposed person after incubation (E → I)."""

        # Only infect if exposed
        if self.state == State.EXPOSED:
            self.state = State.INFECTED
            self.infected_time = time
            self.just_infected = True
            self.days_infected = 0

    def recover(self):
        """ Recover an infected person (I → R)."""

        # only recover if infected
        if self.state == State.INFECTED:
            self.state = State.RECOVERED
            self.just_recovered = True