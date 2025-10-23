class Virus:
    """ Class representing a virus with its properties."""

    def __init__(self, name: str, infect_rate: float, cure_rate: float, infection_time: int):
        """ Initialize with name, infection rate, cure rate, and time infected."""
        
        # Initializes Virus fields from passed in from the config file in the Simulation class.
        self.name = name
        self.infect_rate = infect_rate
        self.cure_rate = cure_rate
        self.infection_time = infection_time
