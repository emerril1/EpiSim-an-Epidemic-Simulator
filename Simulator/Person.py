from EnumeratedTypes import State

class Person:
    """Represents one individual in the population and their health state."""

    def __init__(self, id):
        """Initialize a person with a unique ID and default to susceptible."""

        self.id = id
        self.state = State.SUSCEPTIBLE
        self.exposed_time = None
        self.infected_time = None
        self.vaccinated = False
        self.vaccine_effectiveness = 0.0
        self.isolated = False

    def expose(self, time):
        """Expose a susceptible person to the virus (S → E)."""

        if self.state == State.SUSCEPTIBLE:
            self.state = State.EXPOSED
            self.exposed_time = time

    def infect(self, time):
        """Infect an exposed person after incubation (E → I)."""

        if self.state == State.EXPOSED:
            self.state = State.INFECTED
            self.infected_time = time

    def recover(self):
        """Recover an infected person (I → R)."""

        if self.state == State.INFECTED:
            self.state = State.RECOVERED