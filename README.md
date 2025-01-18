# Telecom Network Simulator

This repository contains a Python-based Telecom Network Simulator designed to model and analyze the behavior of telecommunication networks. The simulator helps understand network dynamics, performance metrics, and traffic flow within telecom systems.

## Features

- **Network Component Simulation**: Models various network components such as base stations, routers, and user devices.
- **Traffic Modeling**: Simulates data traffic between devices within the network.
- **Performance Metrics**: Provides key performance indicators for comprehensive analysis.
- **Modularity**: Offers a scalable and modular design for easy customization and extension.

## Prerequisites

Ensure you have the following installed:

- **Python**: Version 3.7 or later.
- **Required Libraries**: Listed in the `requirements.txt` file.

Install the dependencies using:

```bash
pip install -r requirements.txt
```
## main.py
The main.py script is the entry point for the Telecom Network Simulator. It orchestrates the entire simulation process, performing the following steps:

**Create Network Topology:**

Constructs the network's structure using the NetworkTopology class.
Visualizes the created network topology.

**Simulate Normal Traffic:**

Generates and logs normal network traffic before introducing any disruptions.
Saves traffic logs in the results/normal_traffic_logs.csv file.

**Introduce Bottlenecks:**

Simulates network bottlenecks using the BottleneckSimulation class.
Introduces multiple bottlenecks and logs them in the results/bottleneck_logs.csv file.

**Simulate Post-Bottleneck Traffic:**

Generates and logs network traffic after bottlenecks have been introduced.
Saves the post-bottleneck traffic logs in the results/post_bottleneck_traffic_logs.csv file.

**Completion:**

Notifies the user that the simulation is complete and directs them to the results directory for detailed logs.
This script provides a comprehensive workflow to analyze network behavior under normal and bottlenecked conditions, making it useful for performance evaluation and troubleshooting.


**Run the main.py file using:**

```bash
python main.py
```
