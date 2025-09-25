from EnumeratedTypes import State

# Class representing a person in the simulation. 
# Can either be susceptible, infected, or recovered.
# Functions to infect or cure the person.

class Person:
    _id = 0
    state = []

    # Initialize a person with a unique ID and susceptible state.
    def __init__(self):
        Person._id += 1
        self.id = Person._id
        self.state = State.SUSCEPTIBLE
        self.infection_time = None
    
    # Function to infect the person, changing their state from susceptible to infected.
    def infect(self, time: int):
        if self.state == State.SUSCEPTIBLE:
            self.state = State.INFECTED
            self.infection_time = time
    
    # Function to cure the person, changing their state from infected to recovered.
    def cure(self, time: int):
        if self.state == State.INFECTED:
            self.state = State.RECOVERED
            self.infection_time = time