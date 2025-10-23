from enum import Enum, auto

class State(Enum):
    """ Different states a person can be in during the simulation. Represents traditional SIER compartmental model."""
    
    SUSCEPTIBLE = auto()
    EXPOSED = auto()
    INFECTED = auto()
    RECOVERED = auto()

class InterventionType(Enum):
    """ Different types of interventions that can be applied in the simulation."""
    
    VACCINE = auto()
    QUARANTINE = auto()
    SOCIAL_DISTANCING = auto()
    
