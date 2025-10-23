# Simidemic: An Epidemic Simulator

“Simidemic: An Epidemic Simulator” falls within the domain of epidemiology and computational modeling. Specifically, it focuses on simulating infectious disease spread within a controlled, virtual population to study dynamics of transmission and intervention strategies.

Understanding how infectious diseases spread and how intervention strategies can mitigate outbreaks is critical for public health planning not just locally, but globally. However, real-world experimentation is often impractical, unethical, or even highly unfeasible. Therefore, computational simulations are needed that model disease transmission, evaluate infection rates, and assess the effectiveness of intervention strategies in a controlled environment.

The simulation will:
* Model infection dynamics using a compartmental approach (e.g., susceptible, exposed, infected, recovered).
* Track infection rates over time.
* Evaluate the effectiveness of basic intervention strategies (e.g., social distancing, vaccination, quarantine).

The simulation will not:
* Differentiate between types of pathogens such as bacteria, parasites, or fungi.
* Model complex social, environmental, or biological factors beyond random interactions within the population.

By focusing on a simplified virus model, this simulation aims to provide insights into disease propagation and containment strategies, offering a foundation for understanding more complex epidemiological scenarios.

# Project Status

The epidemic simulator is now feature complete and more realistic than before. All main systems such as population modeling, infection logic, and interventions, are fully implemented and documented. The simulator now supports external configuration files for setting parameters such as population size, infection rate, cure rate, and simulation duration, removing the need for hardcoded values.

Recent updates have introduced major improvements to both accuracy and usability:
* Expanded Interventions: Vaccination, quarantine, and a new social distancing strategy using the adjust_contact_rate function let users test multiple outbreak control methods.
* Enhanced Population Modeling: A small world network and new helper functions like assign_age_group and update provide more lifelike human interaction patterns and age-based effects.
* Data and Visualization: The simulator now exports detailed time series, event logs, and summary reports, with visual graphs showing epidemic curves and intervention impacts.

These additions build on the original design without changing its goals. The result is a more configurable, data-rich, and realistic simulator that better models how an epidemic spreads and responds to interventions.

# Installation Instructions

This simulation was developed using Python version 3.13. While this is not the absolute latest release, it was chosen to ensure compatibility with the NetworkX package. NetworkX is supported on Python versions 3.11 and above, making 3.13 a stable and reliable choice for this project.

The latest Python version can always be downloaded from the official Python website: https://www.python.org/downloads/

The NetworkX library is required to generate and manage the population contact graph within the simulation.
* In this project, NetworkX was installed directly through the Visual Studio Code terminal, but it can be installed in any IDE or editor that supports Python.
* If the terminal installation does not work, NetworkX can also be downloaded and unpacked manually.

1.Standard Installation (recommended)

From a terminal or command prompt, run:
- `pip install networkx`

Official installation instructions are available here: https://networkx.org/documentation/stable/install.html

2.Manual Installation (alternative method)

If direct installation fails, the package can be downloaded and installed manually:
* GitHub release page: https://github.com/networkx/networkx/releases
* PyPI package page: https://pypi.python.org/pypi/networkx

This ensures the simulation has all the necessary dependencies to run properly, regardless of environment or editor.

# Usage

All key parameters for the simulator are defined in the config.json file located in the project root. This file allows users to adjust settings such as population size, virus characteristics, intervention strategies, and simulation duration without changing the source code. Each value can be modified to test different outbreak conditions and intervention effects.

Once the configuration file is updated and placed in the correct directory, the simulation can be run from any environment or IDE that supports Python. The simulator will automatically read the configuration, initialize all components, and begin execution.

After completion, several output files are generated automatically. These include:
* timeseries.csv – Daily counts of Susceptible, Exposed, Infected, and Recovered individuals.
* events.csv – Detailed logs of individual transitions, including infection and recovery events.
* summary.json – Key statistics and metadata for the entire simulation run.
* curve.png - Detailed plot curve of each compartmen of the SEIR model.

These files provide a complete record of the simulation’s behavior and can be used for further analysis or reporting.

# Architecture Overview

The simulator is made up of six main classes and a main program: EnumeratedTypes, Virus, Person, Intervention, Population, and Simulation.

The Virus class stores disease details such as infection rate, cure rate, and the time it takes for exposed individuals to become infectious.

The Person class represents an individual with an ID, health state, and age group. Each person begins as Susceptible and can transition between states through functions that handle exposure, infection, recovery, and quarantine.

The Intervention class manages the different public health strategies: vaccination, quarantine, and social distancing. Each intervention has its own start day, coverage, and reduction settings. When triggered, these functions adjust population behavior, such as isolating infected people or reducing contact rates.

The Population class controls all individuals and their interactions through a small-world network that mimics real social contact patterns. Key functions include assign_age_group, adjust_contact_rate, and update, which handle infection spread and recovery each day.

The Simulation class coordinates the entire process, running the epidemic step by step, applying interventions, and exporting time series, event logs, and summary reports.

Lastly, EnumeratedTypes defines all possible health states, improving organization and readability. Overall, the architecture remains consistent with the original design but now includes more realistic modeling, better configurability, and improved data tracking.