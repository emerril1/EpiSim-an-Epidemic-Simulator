class Virus:
    ''' Class representing a virus with its properties.'''

    def __init__(self, name: str, infect_rate: float, cure_rate: float):
        ''' Initialize with name, infection rate, and cure rate.'''
        
        self.name = name
        self.infect_rate = infect_rate
        self.cure_rate = cure_rate

    
