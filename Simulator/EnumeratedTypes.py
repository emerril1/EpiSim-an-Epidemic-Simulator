from enum import Enum, auto

class State(Enum):
    SUSCEPTIBLE = auto()
    INFECTED = auto()
    RECOVERED = auto()

class InterventionType(Enum):
    VACCINE = auto()
    QUARANTINE = auto()
    SOCIAL_DISTANCING = auto()
    