import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Create a random graph with 100 nodes and a probability of 0.05 for edge creation
G = nx.erdos_renyi_graph(100, 0.05)

# Initialize the status of each node to 'S' (susceptible)
status = {node: 'S' for node in G.nodes}

# Randomly select 5 nodes to be initially infected
initial_infected = random.sample(list(G.nodes), 5)
for node in initial_infected:
    status[node] = 'I'

# Define infection and recovery rates
infection_rate = 0.1
recovery_rate = 0.05


def simulate_step(status):
    new_status = status.copy()
    for node in G.nodes:
        if status[node] == 'I':
            for neighbor in G.neighbors(node):
                if status[neighbor] == 'S' and random.random() < infection_rate:
                    new_status[neighbor] = 'I'
            if random.random() < recovery_rate:
                new_status[node] = 'R'
    return new_status


# Number of simulation steps
steps = 20

# Run the simulation and store the status at each step
status_history = [status]
for step in range(steps):
    status = simulate_step(status)
    status_history.append(status)

# Set up the figure and axis
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.25)


# Function to update the graph for each frame
def update(val):
    step = int(slider.val)
    current_status = status_history[step]
    color_map = {'S': 'blue', 'I': 'red', 'R': 'green'}
    node_colors = [color_map[current_status[node]] for node in G.nodes]
    ax.clear()
    nx.draw(G, node_color=node_colors, with_labels=False, ax=ax)
    ax.set_title(f"Step {step}")


# Create the slider
ax_slider = plt.axes([0.1, 0.1, 0.8, 0.05], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Step', 0, steps, valinit=0, valstep=1)

# Update the plot when the slider value changes
slider.on_changed(update)

# Initial plot
update(0)

# Display the plot
plt.show()
