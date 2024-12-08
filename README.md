## 5800 Final Project Sec19 Team2B
### Topic:
Preliminary Simulation and Prediction Model of the Pandemic Disease COVID-19
### Introduction:
This is our final project for 5800 Algorithm. We developed a preliminary simulation and prediction model for the COVID-19 pandemic. The model simulates the spread of the virus within different regions, specifically focusing on British Columbia (BC) and Vancouver. The simulation used a network-based approach to model the interactions between individuals within various communities, and the prediction used a Sequential neural network model. The project includes the following key components:

**1. Community Graph Generation:**

The project generates Barabási-Albert graphs for each community based on population size and density. These graphs represent the social network within each community.

**2. Inter-Regional Connections:**

The model combines individual community graphs into a single graph, adding inter-regional connections to simulate interactions between different communities.

**3. Infection Simulation:**

The simulation models the spread of the virus over time, considering factors such as infection rate, recovery rate, mortality rate, and incubation period. The model also accounts for mutations in the virus at specified intervals.

**4. Reporting and Visualization:**

The project provides weekly reports on new cases, cumulative cases, and deaths. It also includes various visualization options, such as line graphs, interactive dot graphs, and GeoJSON maps, to help users understand the spread of the virus.

**5. Command Line Interface:**

Users can choose the region (BC or Vancouver) and the type of visualization (line or dot) through command line arguments, making the simulation flexible and user-friendly.

This project serves as a valuable tool for understanding the dynamics of COVID-19 spread and can be used to inform public health decisions and strategies.

---

## Team Members:
| Icon                                                                                                 | Name                                                       | Email                        |
| ----------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------- |
| <img src="https://avatars.githubusercontent.com/u/126201955" alt="Jiahuan He" height="64" width="64"> | <a href="https://github.com/nakurahe">Jiahuan He</a>       | he.jiahuan@northeastern.edu  |
| <img src="https://avatars.githubusercontent.com/u/169320555" alt="Michelle Cong" height="64" width="64"> | <a href="https://github.com/michellecong">Michelle Cong</a>       | cong.m@northeastern.edu  |
| <img src="https://avatars.githubusercontent.com/u/62527532" alt="Ya Wang" height="64" width="64"> | <a href="https://github.com/nnnnnnnf">Ya Wang</a>       | wang.ya1@northeastern.edu      |
| <img src="https://avatars.githubusercontent.com/u/166670701" alt="Jane Feng" height="64" width="64"> | <a href="https://github.com/wang88888888888888">Jane Feng</a> | feng.chenc@northeastern.edu |
