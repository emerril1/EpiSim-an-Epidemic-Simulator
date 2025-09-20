from EnumeratedTypes import State

class Person:
    _id = 0
    state = []

    def __init__(self):
        Person._id += 1
        self.id = Person._id
        self.state = State.SUSCEPTIBLE
        self.infection_time = None
    
    def infect(self, time: int):
        if self.state == State.SUSCEPTIBLE:
            self.state = State.INFECTED
            self.infection_time = time
    
    def cure(self, time: int):
        if self.state == State.INFECTED:
            self.state = State.RECOVERED
            self.infection_time = time