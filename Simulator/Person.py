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
    
    def infect(self, time):
        ''' Function to infect the person, changing their state to infected.'''
        
        self.state = State.INFECTED
        self.infected_time = time
    
    def cure(self):
        ''' Function to cure the person, changing their state to recovered.'''
        
        self.state = State.RECOVERED

    def expose(self, time):
        ''' Function to expose the person, changing their state to exposed.'''

        self.state = State.EXPOSED
        self.exposed_time = time