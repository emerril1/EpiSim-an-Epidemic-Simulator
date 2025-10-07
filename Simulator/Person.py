from EnumeratedTypes import State

class Person:
    ''' Class representing a person in the simulation. Can either be susceptible, infected, or recovered.
        Functions to infect or cure the person. '''
    
    _id = 0
    state = []

    def __init__(self):
        ''' Initialize a person with a unique ID and susceptible state.'''
        
        Person._id += 1
        self.id = Person._id
        self.state = State.SUSCEPTIBLE
        self.infection_time = None
    
    def infect(self, time: int):
        ''' Function to infect the person, changing their state from susceptible to infected.'''
        
        if self.state == State.SUSCEPTIBLE:
            self.state = State.INFECTED
            self.infection_time = time
    
    def cure(self, time: int):
        ''' Function to cure the person, changing their state from infected to recovered.'''
        
        if self.state == State.INFECTED:
            self.state = State.RECOVERED
            self.infection_time = time
