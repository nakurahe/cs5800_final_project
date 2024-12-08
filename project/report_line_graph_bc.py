import argparse
from typing import Tuple
import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import pandas as pd


# Constants for BC/ Vancouver
# Population density of BC cities
BC_POPULATION_DENSITY = [
    {"name": "Abbotsford", "population": 15352, "density": 2},
    {"name": "Armstrong", "population": 532, "density": 3},
    {"name": "Burnaby", "population": 24912, "density": 6},
    {"name": "Campbell River", "population": 3551, "density": 1},
    {"name": "Castlegar", "population": 833, "density": 2},
    {"name": "Chilliwack", "population": 9320, "density": 2},
    {"name": "Colwood", "population": 1896, "density": 3},
    {"name": "Coquitlam", "population": 14862, "density": 3},
    {"name": "Courtenay", "population": 2842, "density": 2},
    {"name": "Cranbrook", "population": 2049, "density": 2},
    {"name": "Dawson Creek", "population": 1232, "density": 2},
    {"name": "Delta", "population": 10845, "density": 2},
    {"name": "Duncan", "population": 504, "density": 5},
    {"name": "Enderby", "population": 302, "density": 2},
    {"name": "Fernie", "population": 632, "density": 2},
    {"name": "Fort St. John", "population": 2146, "density": 2},
    {"name": "Grand Forks", "population": 411, "density": 2},
    {"name": "Greenwood", "population": 70, "density": 1},
    {"name": "Kamloops", "population": 9790, "density": 2},
    {"name": "Kelowna", "population": 14457, "density": 2},
    {"name": "Kimberley", "population": 811, "density": 1},
    {"name": "Langford", "population": 4658, "density": 3},
    {"name": "Langley", "population": 2896, "density": 6},
    {"name": "Maple Ridge", "population": 9099, "density": 2},
    {"name": "Merritt", "population": 705, "density": 1},
    {"name": "Mission", "population": 4151, "density": 1},
    {"name": "Nanaimo", "population": 9986, "density": 3},
    {"name": "Nelson", "population": 1110, "density": 3},
    {"name": "New Westminster", "population": 7891, "density": 9},
    {"name": "North Vancouver", "population": 5812, "density": 9},
    {"name": "Parksville", "population": 1364, "density": 3},
    {"name": "Penticton", "population": 3688, "density": 2},
    {"name": "Pitt Meadows", "population": 1914, "density": 1},
    {"name": "Port Alberni", "population": 1825, "density": 3},
    {"name": "Port Coquitlam", "population": 6149, "density": 4},
    {"name": "Port Moody", "population": 3353, "density": 3},
    {"name": "Powell River", "population": 1394, "density": 2},
    {"name": "Prince George", "population": 7670, "density": 1},
    {"name": "Prince Rupert", "population": 1230, "density": 1},
    {"name": "Quesnel", "population": 988, "density": 1},
    {"name": "Revelstoke", "population": 827, "density": 1},
    {"name": "Richmond", "population": 20993, "density": 4},
    {"name": "Rossland", "population": 414, "density": 1},
    {"name": "Salmon Arm", "population": 1943, "density": 1},
    {"name": "Surrey", "population": 56832, "density": 4},
    {"name": "Terrace", "population": 1201, "density": 1},
    {"name": "Trail", "population": 792, "density": 1},
    {"name": "Vancouver", "population": 66224, "density": 11},
    {"name": "Vernon", "population": 4451, "density": 2},
    {"name": "Victoria", "population": 9186, "density": 9},
    {"name": "West Kelowna", "population": 3607, "density": 1},
    {"name": "White Rock", "population": 2193, "density": 8},
    {"name": "Williams Lake", "population": 1094, "density": 2}
]

# Population density of Vancouver neighborhoods
VAN_POPULATION_DENSITY_REDUCED = [
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

VAN_POPULATION_DENSITY_FULL = [
    {"name": "Arbutus-Ridge", "population": 16121, "density": 3},
    {"name": "Downtown", "population": 65380, "density": 12},
    {"name": "Dunbar-Southlands", "population": 22582, "density": 2},
    {"name": "Fairview", "population": 35435, "density": 7},
    {"name": "Grandview-Woodland", "population": 30750, "density": 5},
    {"name": "Hastings-Sunrise", "population": 36442, "density": 3},
    {"name": "Kensington-Cedar Cottage", "population": 51989, "density": 5},
    {"name": "Kerrisdale", "population": 14730, "density": 2},
    {"name": "Killarney", "population": 30909, "density": 3},
    {"name": "Kitsilano", "population": 45369, "density": 6},
    {"name": "Marpole", "population": 24460, "density": 3},
    {"name": "Mount Pleasant", "population": 34735, "density": 6},
    {"name": "Oakridge", "population": 13734, "density": 2},
    {"name": "Renfrew-Collingwood", "population": 54313, "density": 5},
    {"name": "Riley Park", "population": 23773, "density": 3},
    {"name": "Shaughnessy", "population": 8885, "density": 1},
    {"name": "South Cambie", "population": 8400, "density": 3},
    {"name": "Strathcona", "population": 13265, "density": 2},
    {"name": "Sunset", "population": 38471, "density": 4},
    {"name": "Victoria-Fraserview", "population": 32743, "density": 4},
    {"name": "West End", "population": 49749, "density": 17},
    {"name": "West Point Grey", "population": 13771, "density": 2}
]

# Inter-regional connections
INTER_REGION_CONNECTIONS = {
    "BC": 1145,
    "Vancouver": 55
}

# COVID-19 Simulation Parameters
# Initial infection rate, recovery rate, mortality rate, incubation period, and mutation weeks
INITIAL_INFECTION_RATE = 0.15
RECOVERY_RATE = 0.9
MORTALITY_RATE = 0.01
INCUBATION_PERIOD = 5
MUTATION_WEEKS = [48, 96]
MUTATION_RATE = 1.2


def create_community_graph(
        density_list=VAN_POPULATION_DENSITY_REDUCED,
        inter_region_connections=INTER_REGION_CONNECTIONS["Vancouver"]) -> nx.Graph:
    # Create a community graph using barabasi_albert_graph theory
    community_graphs = [
        nx.barabasi_albert_graph(each_city["population"], each_city["density"])
        for each_city in density_list
    ]
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
        if idx < len(community_graphs) - 1:
            for _ in range(inter_region_connections):
                node_a = random.choice(list(community.nodes))
                node_b = random.choice(
                    list(community_graphs[idx + 1].nodes)) + offset
                G.add_edge(node_a, node_b)
    return G


# Initialize Infection Status
def get_initial_infection_status(G: nx.Graph, num_initial_infections=20) -> Tuple[dict[str, str], list]:
    initialLinfection_status_dict = {node: 'S' for node in G.nodes}
    # Initial infections
    initial_infected_nodes = random.sample(list(G.nodes), num_initial_infections)
    for node in initial_infected_nodes:
        initialLinfection_status_dict[node] = 'E'
    return initialLinfection_status_dict, initial_infected_nodes

# Weekly Reporting
def simulate_week(G: nx.Graph,
                  infection_status_dict: dict[str, str],
                  exposed_duration: dict[str, int],
                  infection_rate) -> dict[str, list[int]]:
    new_cases = 0
    deaths = 0

    for _ in range(7):  # Simulate 7 days per week
        new_infection_status_dict = infection_status_dict.copy()

        for node in G.nodes:
            if infection_status_dict[node] == 'E':
                exposed_duration[node] += 1
                if exposed_duration[node] >= INCUBATION_PERIOD:
                    new_infection_status_dict[node] = 'I'
                    new_cases += 1

            elif infection_status_dict[node] == 'I':
                # Infect neighbors
                for neighbor in G.neighbors(node):
                    if infection_status_dict[neighbor] == 'S' and random.random() < infection_rate:
                        new_infection_status_dict[neighbor] = 'E'

                # Death or Recovery
                if random.random() < MORTALITY_RATE:
                    new_infection_status_dict[node] = 'D'
                    deaths += 1
                elif random.random() < RECOVERY_RATE:
                    new_infection_status_dict[node] = 'R'
        infection_status_dict.update(new_infection_status_dict)

    return new_cases, deaths


def get_status_history(G: nx.Graph, initial_infection_status_dict: dict, initial_infected: list, total_weeks: int):
    cumulative_cases = len(initial_infected)
    weekly_data = {
        'new_cases': [],
        'cumulative_cases': [],
        'deaths': [],
        'infection_status_dict_snapshots': [],
    }
    infection_status_dict = initial_infection_status_dict.copy()
    exposed_duration_dict = {node: 0 for node in G.nodes}
    infection_rate = INITIAL_INFECTION_RATE

    for week in range(total_weeks):
        # Mutation Effect
        if week in MUTATION_WEEKS:
            infection_rate *= MUTATION_RATE

        new_cases, deaths = simulate_week(G, infection_status_dict, exposed_duration_dict, infection_rate)
        cumulative_cases += new_cases

        weekly_data['new_cases'].append(new_cases)
        weekly_data['cumulative_cases'].append(cumulative_cases)
        weekly_data['deaths'].append(deaths)
        weekly_data['infection_status_dict_snapshots'].append(infection_status_dict.copy())
    return weekly_data


# Print Weekly Report
def print_weekly_report(weekly_data: dict, total_weeks: int):
    print("Weekly Report:")
    for week in range(total_weeks):
        print(f"Week {week + 1}: New Cases = {weekly_data['new_cases'][week]}, "
              f"Cumulative Cases = {weekly_data['cumulative_cases'][week]}, "
              f"Deaths = {weekly_data['deaths'][week]}")


# Visualization
def visualize_simulation_line_graph(G: nx.Graph,
                         weekly_data: dict, # {'new_cases': list[int], 'cumulative_cases': list[int], 'deaths': list[int], 'infection_status_dict_snapshots': list[dict]}
                         total_weeks: int):
    weeks_range = range(1, total_weeks + 1)
    # Plot case variance line graph
    weekly_df = pd.DataFrame({
        'Week': weeks_range,
        'New Cases': weekly_data['new_cases'],
        'Cumulative Cases': weekly_data['cumulative_cases'],
        'Deaths': weekly_data['deaths']
    })
    weekly_df.plot(title='COVID-19 Weekly Report for Vancouver Simulation',
                   x = 'Week',
                   y = ['New Cases', 'Cumulative Cases', 'Deaths'],
                   legend=True,
                   grid=True)
    plt.show()



def visualize_simulation_dotted_graph(G: nx.Graph,
                                      infection_status_dict_snapshots: list[dict],
                                      total_weeks: int):
    # Plow an interactive graph in a new figure
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.1, bottom=0.25)

    # Create the slider
    ax_slider = plt.axes([0.1, 0.1, 0.8, 0.05], facecolor='lightgoldenrodyellow')
    slider = Slider(ax_slider, 'Week', 0, total_weeks, valinit=0, valstep=1)

    def slider_update(val):
        week = int(val)
        current_infection_status_dict = infection_status_dict_snapshots[week]
        color_map = {'S': 'blue', 'E': 'orange', 'I': 'red', 'R': 'green', 'D': 'black'}
        node_colors = [color_map[current_infection_status_dict[node]] for node in G.nodes]

        ax.clear()
        nx.draw(G, node_color=node_colors, with_labels=False, node_size=10, ax=ax, edge_color='none')
        ax.set_title(f"Week {week}")

        # Adding a legend
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Susceptible'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=10, label='Exposed'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Infected'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Recovered'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=10, label='Dead')
        ]
        ax.legend(handles=legend_elements, loc='upper right')

    # Update the graph when the slider value changes
    slider.on_changed(slider_update)

    # Initialize interactive graph
    slider_update(0)

    # Show all plots
    plt.show()


def main():
    parser = argparse.ArgumentParser(description='COVID-19 Simulation for BC or Vancouver')
    parser.add_argument('--region', type=str, choices=['bc', 'vancouver', 'vancouver_full'], required=True, help='Choose the region to simulate (bc, vancouver, or vancouver_full)')
    args = parser.parse_args()
    draw_dot_graph = True

    if args.region == 'bc':
        population_density = BC_POPULATION_DENSITY
        inter_region_connection = INTER_REGION_CONNECTIONS['BC']
        draw_dot_graph = False
    elif args.region == 'vancouver':
        population_density = VAN_POPULATION_DENSITY_REDUCED
        inter_region_connection = INTER_REGION_CONNECTIONS['Vancouver']
    elif args.region == 'vancouver_full':
        population_density = VAN_POPULATION_DENSITY_FULL
        inter_region_connection = INTER_REGION_CONNECTIONS['Vancouver']

    # Simulate 52 * 3 = 156 weeks (3 years)
    total_weeks = 156
    num_initial_infections = 20
    G = create_community_graph(population_density, inter_region_connection)
    initial_infection_status_dict, initial_infected = get_initial_infection_status(G, num_initial_infections)
    weekly_data = get_status_history(G, initial_infection_status_dict, initial_infected, total_weeks)
    print_weekly_report(weekly_data, total_weeks)
    visualize_simulation_line_graph(G, weekly_data, total_weeks)
    if (draw_dot_graph):
        visualize_simulation_dotted_graph(G, weekly_data['infection_status_dict_snapshots'], total_weeks)

if __name__ == "__main__":
    main()