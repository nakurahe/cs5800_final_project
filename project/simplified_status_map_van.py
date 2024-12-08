import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import pandas as pd

# Constants for BC
# BC population in 2021:
num_nodes = 3327824
# 53 cities in BC
num_communities = 53
# Population density of BC cities
van_population_density = [
    {"name": "Arbutus-Ridge", "population": 161, "density": 3},
    {"name": "Downtown", "population": 653, "density": 12},
    {"name": "Dunbar-Southlands", "population": 225, "density": 2},
    {"name": "Fairview", "population": 354, "density": 7},
    {"name": "Grandview-Woodland", "population": 307, "density": 5},
    {"name": "Hastings-Sunrise", "population": 364, "density": 3},
    {"name": "Kensington-Cedar Cottage", "population": 519, "density": 5},
    {"name": "Kerrisdale", "population": 147, "density": 2},
    {"name": "Killarney", "population": 309, "density": 3},
    {"name": "Kitsilano", "population": 453, "density": 6},
    {"name": "Marpole", "population": 244, "density": 3},
    {"name": "Mount Pleasant", "population": 347, "density": 6},
    {"name": "Oakridge", "population": 137, "density": 2},
    {"name": "Renfrew-Collingwood", "population": 543, "density": 5},
    {"name": "Riley Park", "population": 237, "density": 3},
    {"name": "Shaughnessy", "population": 88, "density": 1},
    {"name": "South Cambie", "population": 84, "density": 3},
    {"name": "Strathcona", "population": 132, "density": 2},
    {"name": "Sunset", "population": 384, "density": 4},
    {"name": "Victoria-Fraserview", "population": 327, "density": 4},
    {"name": "West End", "population": 497, "density": 17},
    {"name": "West Point Grey", "population": 137, "density": 2}
]

# COVID-19 Simulation Parameters
# Initial infection rate, recovery rate, mortality rate, incubation period, and mutation weeks
infection_rate = 0.15
recovery_rate = 0.9
mortality_rate = 0.01
incubation_period = 5
mutation_weeks = [48, 96]
mutation_rate = 1.2

# City-specific parameters
community_graphs = [
    nx.barabasi_albert_graph(
        each_city["population"],
        each_city["density"]) for each_city in van_population_density]

# Combine regions into a single graph with inter-regional connections
G = nx.Graph()
offset = 0
for idx, community in enumerate(community_graphs):
    # Renumber nodes to prevent conflicts
    mapping = {node: node + offset for node in community.nodes}
    community = nx.relabel_nodes(community, mapping)
    G = nx.compose(G, community)
    offset += community.number_of_nodes()

    # Inter-region connections
    if idx < num_communities - 1:
        for _ in range(50):  # Randomly connect 50 edges between regions
            node_a = random.choice(list(community.nodes))
            node_b = random.choice(list(community_graphs[idx + 1].nodes)) + offset
            G.add_edge(node_a, node_b)

# Initialize Infection Status
status = {node: 'S' for node in G.nodes}
initial_infected = random.sample(list(G.nodes), 20)  # Initial infections
for node in initial_infected:
    status[node] = 'E'

# COVID-19 Simulation Parameters
infection_rate = 0.15  # Initial infection rate
recovery_rate = 0.9
mortality_rate = 0.01
incubation_period = 5  # Days before symptoms
mutation_weeks = [48, 96]  # Weeks when virus mutates

# Weekly Reporting
weekly_data = {'new_cases': [], 'cumulative_cases': [], 'deaths': []}
exposed_duration = {node: 0 for node in G.nodes}
cumulative_cases = len(initial_infected)


def simulate_week(status, exposed_duration):
    global infection_rate, cumulative_cases
    new_cases = 0
    deaths = 0

    for _ in range(7):  # Simulate 7 days per week
        new_status = status.copy()

        for node in G.nodes:
            if status[node] == 'E':
                exposed_duration[node] += 1
                if exposed_duration[node] >= incubation_period:
                    new_status[node] = 'I'
                    new_cases += 1

            elif status[node] == 'I':
                # Infect neighbors
                for neighbor in G.neighbors(node):
                    if status[neighbor] == 'S' and random.random() < infection_rate:
                        new_status[neighbor] = 'E'

                # Death or Recovery
                if random.random() < mortality_rate:
                    new_status[node] = 'D'
                    deaths += 1
                elif random.random() < recovery_rate:
                    new_status[node] = 'R'

        status = new_status

    # Mutation Effect
    current_week = len(weekly_data['new_cases'])
    if current_week in mutation_weeks:
        infection_rate *= 1.2  # Increase infection rate by 20% for mutations

    cumulative_cases += new_cases
    weekly_data['new_cases'].append(new_cases)
    weekly_data['cumulative_cases'].append(cumulative_cases)
    weekly_data['deaths'].append(deaths)

    return status


# Simulate over 12 weeks
weeks = 200
status_history = [status]
for week in range(weeks):
    status = simulate_week(status, exposed_duration)
    status_history.append(status)

# Convert weekly data to DataFrame for better display
weekly_df = pd.DataFrame({
    'Week': list(range(1, weeks + 1)),
    'New Cases': weekly_data['new_cases'],
    'Cumulative Cases': weekly_data['cumulative_cases'],
    'Deaths': weekly_data['deaths']
})


# Visualization Setup
def update(val):
    step = int(slider.val)
    current_status = status_history[step]
    color_map = {'S': 'blue', 'E': 'orange', 'I': 'red', 'R': 'green', 'D': 'black'}
    node_colors = [color_map[current_status[node]] for node in G.nodes]

    ax.clear()
    nx.draw(G, node_color=node_colors, with_labels=False, node_size=10, ax=ax, edge_color='none')
    ax.set_title(f"Week {step}")

    # Adding a legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Susceptible'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=10, label='Exposed'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Infected'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Recovered'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=10, label='Dead')
    ]
    ax.legend(handles=legend_elements, loc='upper right')


# Set up the figure and axis
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.25)

# Create the slider
ax_slider = plt.axes([0.1, 0.1, 0.8, 0.05], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Week', 0, weeks, valinit=0, valstep=1)

# Update the plot when the slider value changes
slider.on_changed(update)

# Initial plot
update(0)

# Display the plot
plt.show()
