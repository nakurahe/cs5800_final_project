import networkx as nx
import random
import pandas as pd
import folium
import geopandas as gpd
import branca
from constants import VAN_POPULATION_DENSITY_REDUCED


# Initialize a dictionary to store node-community mappings
node_community_map = {}

# Generate a Barabási-Albert graph for each community based on its population size
community_graphs = [
    nx.barabasi_albert_graph(each_community["population"], each_community["density"])
    for each_community in VAN_POPULATION_DENSITY_REDUCED
]

# Combine regions into a single graph with inter-regional connections
G = nx.Graph()
offset = 0
num_communities = len(community_graphs)
community_names = [community["name"] for community in VAN_POPULATION_DENSITY_REDUCED]

for idx, community in enumerate(community_graphs):
    community_name = community_names[idx]

    # Renumber nodes to prevent conflicts
    mapping = {node: node + offset for node in community.nodes}
    community = nx.relabel_nodes(community, mapping)

    # Update node-community mapping with the current community name
    for node in community.nodes:
        node_community_map[node] = community_name

    # Add the current community graph to the main graph
    G = nx.compose(G, community)
    offset += community.number_of_nodes()

    # Inter-region connections
    if idx < num_communities - 1:
        for _ in range(1145):  # Randomly connect 50 edges between regions
            node_a = random.choice(list(community.nodes))
            node_b = random.choice(list(community_graphs[idx + 1].nodes)) + offset
            G.add_edge(node_a, node_b)

# Initialize Infection Status
status = {node: "S" for node in G.nodes}
initial_infected = random.sample(list(G.nodes), 20)  # Initial infections
for node in initial_infected:
    status[node] = "E"

# COVID-19 Simulation Parameters
infection_rate = 0.15  # Initial infection rate
recovery_rate = 0.9
mortality_rate = 0.01
incubation_period = 5  # Days before symptoms
mutation_days = [336, 672]  # Days when virus mutates

# Daily Reporting
cumulative_cases = len(initial_infected)
exposed_duration = {node: 0 for node in G.nodes}
community_data = {name: {"cumulative_cases": 0} for name in community_names}


def simulate_day(status, exposed_duration):
    global infection_rate, cumulative_cases
    new_cases = 0

    # Temporary storage for today's cases by community
    community_daily_cases = {name: 0 for name in community_names}

    new_status = status.copy()

    for node in G.nodes:
        community_name = node_community_map[
            node
        ]  # Get the community name for the current node

        if status[node] == "E":
            exposed_duration[node] += 1
            if exposed_duration[node] >= incubation_period:
                new_status[node] = "I"
                new_cases += 1
                community_daily_cases[community_name] += 1

        elif status[node] == "I":
            # Infect neighbors
            for neighbor in G.neighbors(node):
                if status[neighbor] == "S" and random.random() < infection_rate:
                    new_status[neighbor] = "E"

            # Death or Recovery
            if random.random() < mortality_rate:
                new_status[node] = "D"
            elif random.random() < recovery_rate:
                new_status[node] = "R"

    # Update community-level cumulative cases
    for name in community_names:
        community_data[name]["cumulative_cases"] += community_daily_cases[name]

    # Mutation Effect
    current_day = len(exposed_duration)
    if current_day in mutation_days:
        infection_rate *= 1.2  # Increase infection rate by 20% for mutations

    cumulative_cases += new_cases

    return new_status


# Function to simulate up to a specified day
def simulate_until_day(target_day):
    global status
    for day in range(1, target_day + 1):
        status = simulate_day(status, exposed_duration)

    # Create a DataFrame with cumulative cases per community
    data = {
        "Community": [name for name in community_names],
        "Cumulative Cases": [
            community_data[name]["cumulative_cases"] for name in community_names
        ],
    }
    df = pd.DataFrame(data)
    return df


# Example usage: Simulate until day 100 and get the report
day = 100  # Specify the day you want the report for
result_df = simulate_until_day(day)
print(f"COVID-19 Cumulative Report for Day {day}:\n")
print(result_df.to_string(index=False))

# transform dataframe to dictionary
cases_data = result_df.set_index("Community")["Cumulative Cases"].to_dict()

# import GeoJSON data
geojson_file = "../data/local-area-boundary.geojson"  # the path of geo file
gdf = gpd.read_file(geojson_file)

# create map
m = folium.Map(location=[49.26454048616976, -123.1310488653851], zoom_start=12)

# add headline of map
title_html = f"""
    <h3 align="center" style="font-size:20px"><b>COVID-19 accumulative cases - day {day} </b></h3>
"""
m.get_root().html.add_child(folium.Element(title_html))

# create color mapping, use the scope of accumulative cases
vmin = min(cases_data.values()) if cases_data else 0
vmax = max(cases_data.values()) if cases_data else 1
colormap = branca.colormap.LinearColormap(
    ["pink", "red", "purple"], vmin=vmin, vmax=vmax
).to_step(n=10)

# iterate GeoJSON data and add color to every region
for _, row in gdf.iterrows():
    # get geometry data of every region
    geom = row["geometry"]
    region_name = row["name"]  #  GeoJSON has "name" field to represent name of region

    # get the cases of this region
    cases = cases_data.get(region_name, 0)

    # set the filling color according to the number of cases
    color = colormap(cases)

    # add polygons
    folium.GeoJson(
        geom,
        style_function=lambda x, color=color: {
            "fillColor": color,  # filling
            "color": "black",  # frame color
            "weight": 2,  # weidth
            "fillOpacity": 0.6,  # transparency
        },
        tooltip=f"{region_name}: {cases}",  # the text of the mouse hovering
    ).add_to(m)

# add color legend
m.add_child(colormap)

# save map as HTML
m.save("map_with_cases.html")

# remind the user
print("the map has been saved as map_with_cases.html, open in a browser")
