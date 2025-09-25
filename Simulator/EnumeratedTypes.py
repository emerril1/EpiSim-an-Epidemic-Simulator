from enum import Enum, auto

# Different states a person can be in during the simulation. Represents traditional SIR model.
class State(Enum):
    SUSCEPTIBLE = auto()
    INFECTED = auto()
    RECOVERED = auto()

# Different types of interventions that can be applied in the simulation.
class InterventionType(Enum):
    VACCINE = auto()
    QUARANTINE = auto()
    SOCIAL_DISTANCING = auto()
    