# Class representing a virus with its properties.

class Virus:
    # Initialize with name, infection rate, and cure rate.
    def __init__(self, name: str, infect_rate: float, cure_rate: float):
        self.name = name
        self.infect_rate = infect_rate
        self.cure_rate = cure_rate

    
