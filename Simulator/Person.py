from EnumeratedTypes import State

class Person:
    ''' Class representing a person in the simulation. Can either be susceptible, infected, or recovered.
        Functions to infect or cure the person. '''
    
    state = []

    def __init__(self, id):
        ''' Initialize a person with a unique ID and susceptible state.'''
        
        self.id = id
        self.state = State.SUSCEPTIBLE
        self.exposed_time = None
        self.infected_time = None
        self.vaccinated = False
        self.vaccine_effectiveness = 0.0
    
    def infect(self, time):
        ''' Function to infect the person, changing their state to infected.'''
        
        if self.state == State.SUSCEPTIBLE:
            self.state = State.EXPOSED
            self.exposed_time = time
    
    def cure(self, time):
        ''' Function to cure the person, changing their state to recovered.'''
        
        if self.state != State.INFECTED:
            self.state = State.INFECTED
            self.infected_time = time

    def expose(self, time):
        ''' Function to expose the person, changing their state to exposed.'''

        if self.state == State.INFECTED:
            self.state = State.RECOVERED