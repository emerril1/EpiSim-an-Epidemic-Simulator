# Simidemic: An Epidemic Simulator

“Simidemic: An Epidemic Simulator” falls within the domain of epidemiology and computational modeling. Specifically, it focuses on simulating infectious disease spread within a controlled, virtual population to study dynamics of transmission and intervention strategies.

Understanding how infectious diseases spread and how intervention strategies can mitigate outbreaks is critical for public health planning not just locally, but globally. However, real-world experimentation is often impractical, unethical, or even highly unfeasible. Therefore, computational simulations are needed that model disease transmission, evaluate infection rates, and assess the effectiveness of intervention strategies in a controlled environment.

The simulation will:
* Model infection dynamics using a compartmental approach (e.g., susceptible, infected, recovered).
* Track infection rates over time.
* Evaluate the effectiveness of basic intervention strategies (e.g., isolation, vaccination).

The simulation will not:
* Differentiate between types of pathogens such as bacteria, parasites, or fungi.
* Model complex social, environmental, or biological factors beyond random interactions within the population.

By focusing on a simplified virus model, this simulation aims to provide insights into disease propagation and containment strategies, offering a foundation for understanding more complex epidemiological scenarios.

# Project Status

Completion of the main simulator and two models is all but done. Main functionality is provided in soruce code with proper simulation and infection logic. That also includes the main documentation for each clas and function. Work is beginning on some new parts to make the simulator more complete and interactive. 

These changes include:
* User Input Options – The simulator will be updated to allow users to configure key parameters (such as population size, infection rate, cure rate, and simulation duration) directly, instead of requiring hardcoded values. This will make the tool more flexible and accessible.
* New Intervention Strategy: Social Distancing – In addition to the existing Vaccine and Quarantine strategies, Social Distancing will be introduced. This intervention will modify the population contact graph to reduce interactions, thereby simulating reduced transmission.
* Visualization with Graphs – A visual output will be added using matplotlib.pyplot to display the compartments (Susceptible, Infected, Recovered) over time. This graph will provide a clear epidemic curve and make the progression of the simulation easier to interpret.

No changes have been made to the original project proposal. The overall structure of the system and its intended goals remain consistent with the original design, with these additions serving as natural extensions to improve usability and analysis.

# Installation Instructions

This simulation was developed using Python version 3.13. While this is not the absolute latest release, it was chosen to ensure compatibility with the NetworkX package. NetworkX is supported on Python versions 3.11 and above, making 3.13 a stable and reliable choice for this project.

The latest Python version can always be downloaded from the official Python website: https://www.python.org/downloads/

The NetworkX library is required to generate and manage the population contact graph within the simulation.
* In this project, NetworkX was installed directly through the Visual Studio Code terminal, but it can be installed in any IDE or editor that supports Python.
* If the terminal installation does not work, NetworkX can also be downloaded and unpacked manually.

1.Standard Installation (recommended)

From a terminal or command prompt, run:
- pip install networkx

Official installation instructions are available here: https://networkx.org/documentation/stable/install.html

2.Manual Installation (alternative method)

If direct installation fails, the package can be downloaded and installed manually:
* GitHub release page: https://github.com/networkx/networkx/releases
* PyPI package page: https://pypi.python.org/pypi/networkx

This ensures the simulation has all the necessary dependencies to run properly, regardless of environment or editor.

# Usage

Currently, there is no user input functionality in the simulation. As a result, any testing or execution must be hardcoded into the main program.

From top to bottom in the code:
* Population size can be adjusted by modifying the size value on line 53.
* Virus properties, which include the name, infection rate, and cure rate, and time till infection can be configured by updating the corresponding values on line 54.
* Intervention strategies (currently only Vaccine and Quarantine) can be tested by uncommenting the relevant function calls on lines 61–62 and 64–65.
* Simulation duration can be set by changing the argument in the run() call on line 67.

Once these parameters are set, the simulator can be executed by clicking Run in any code editor of choice. The output will consist of a line-by-line description of the compartments at each time step (1 step = 1 day). 

For example: Day 10: {'S': 12, 'I': 33, 'R': 5}

# Architecture Overview

The main components of the simulator consist of six classes and a main program. The classes include: EnumeratedTypes, Virus, Person, Intervention, Population, and Simulation.

The Virus class stores information about the virus, such as its name, infection rate, and cure rate. The Virus class also now stores a variable that gives the time till infection (e.g. how many days it takes an exposed person to become infected).

The Person class represents an individual in the population. Each person has a unique ID and a health state, along with functions to become infected or cured. Every person begins in the Susceptible state at the start of a simulation.

The Intervention class defines the execute function, which applies user-selected interventions by modifying the population’s contact graph to simulate different scenarios (e.g. social distancing).

The Population class manages a collection of Person objects and generates a contact graph that models interactions. This graph ensures realistic infection dynamics. It includes two key functions: one to generate the graph and another to retrieve the contacts of a given person (node).

The Simulation class coordinates the epidemic process. It contains methods to advance the simulation step by step, run the simulation over a set period, and track statistics (such as susceptible, infected, and recovered counts). These functions are integrated within the main program, which drives the simulation and records results.

Overall, the architecture of the project closely follows the original UML class and sequence diagrams. The only major modification is the addition of the EnumeratedTypes class, which was separated out to improve modularity. This adjustment also shifted some of the relationships between classes compared to the original UML design.