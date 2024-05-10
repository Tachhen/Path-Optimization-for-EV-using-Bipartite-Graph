import networkx as nx
import matplotlib.pyplot as plt
import random
import math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def min_distance(p, positions, min_dist):
    for pos in positions.values():
        if distance(p, pos) < min_dist:
            return False
    return True

def shortest_path_to_cstation(graph, ev_node):
    cstation_nodes = [node for node in graph.nodes() if 'CStations' in node]
    shortest_paths = {}
    for cstation_node in cstation_nodes:
        try:
            shortest_paths[cstation_node] = nx.shortest_path(graph, source=ev_node, target=cstation_node, weight='weight')
        except nx.NetworkXNoPath:
            continue
    if shortest_paths:
        closest_cstation = min(shortest_paths, key=lambda x: len(shortest_paths[x]))
        shortest_path = shortest_paths[closest_cstation]
        total_weight = sum(graph[shortest_path[i]][shortest_path[i+1]]['weight'] for i in range(len(shortest_path)-1))
        return shortest_path, total_weight
    else:
        return None, None

def simulate_ev_path(graph, ev_node, energy_consumption_rate):
    path, total_distance = shortest_path_to_cstation(graph, ev_node)
    if path:
        energy_spent = total_distance * energy_consumption_rate
        return energy_spent, total_distance
    else:
        return None, None

def simulate_multiple_evs(graph, num_evs, energy_consumption_rate):
    energy_spent_list = []
    total_distance_list = []
    for i in range(num_evs):
        ev_node = f'EVehicles{i+1}'
        energy_spent, total_distance = simulate_ev_path(graph, ev_node, energy_consumption_rate)
        if energy_spent is not None:
            energy_spent_list.append(energy_spent)
            total_distance_list.append(total_distance)
    return energy_spent_list, total_distance_list

while True:
    calculate_option = input("Choose an option:\n1. Calculate distance of a single EV from the nearest charging station.\n2. Calculate average distance of all EVs from their nearest charging stations.\nEnter option number: ")
    if calculate_option in ['1', '2']:
        break
    else:
        print("Invalid input. Please enter 1 or 2.")

while True:
    num_evs = input("Enter the number of EVs on the road: ")
    if num_evs.isdigit() and 1 <= int(num_evs) <= 30:
        num_evs = int(num_evs)
        break
    else:
        print("Invalid input. Please enter a number between 1 and 30.")

# Prompt user to enter the energy consumption rate (kWh/km)
energy_consumption_rate = float(input("Enter the energy consumption rate (kWh/km): "))

roadMap = nx.Graph()

EVehicles = [f'EVehicles{i}' for i in range(1, num_evs + 1)]
CStations = [f'CStations{i}' for i in range(1, 5)]
EmtRoads = [f'EmtRoads{i}' for i in range(1, 25)]

roadMap.add_nodes_from(EVehicles, bipartite=0)  
roadMap.add_nodes_from(EmtRoads, bipartite=1)  
roadMap.add_nodes_from(CStations, bipartite=1) 

cstation_positions = {
    'CStations1': (20, 80),
    'CStations2': (80, 20),
    'CStations3': (80, 80),
    'CStations4': (20, 20)
}

pos = {}
for node in EVehicles + EmtRoads + CStations:
    while True:
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        if min_distance((x, y), pos, 10):
            pos[node] = (x, y)
            break

for station, position in cstation_positions.items():
    pos[station] = position

for node, position in pos.items():
    roadMap.add_node(node, pos=position)

for node in roadMap.nodes():
    if roadMap.nodes[node]['bipartite'] == 0:  
        distances = {other_node: distance(pos[node], pos[other_node]) for other_node in roadMap.nodes() if roadMap.nodes[other_node]['bipartite'] == 1 and node != other_node}  
    elif roadMap.nodes[node]['bipartite'] == 1:  
        distances = {other_node: distance(pos[node], pos[other_node]) for other_node in roadMap.nodes() if roadMap.nodes[other_node]['bipartite'] == 0 and node != other_node}  
    closest_neighbors = sorted(distances, key=distances.get)[:2]
    for neighbor in closest_neighbors:
        weight = random.randint(1, 10)  
        roadMap.add_edge(node, neighbor, weight=weight)

if calculate_option == '1':
    while True:
        ev_node_number = input(f"Enter the EV vehicle number (1-{num_evs}): ")
        if ev_node_number.isdigit() and 1 <= int(ev_node_number) <= num_evs:
            ev_node = f'EVehicles{ev_node_number}'
            energy_spent, total_distance = simulate_ev_path(roadMap, ev_node, energy_consumption_rate)
            if energy_spent is not None:
                shortest_path, _ = shortest_path_to_cstation(roadMap, ev_node)
                print("Shortest path to the closest CStation:", shortest_path)
                print("Total energy spent:", energy_spent)
                
                # Plot bipartite graph for the shortest path to the closest station
                plt.figure(figsize=(10, 10))
                node_colors = ['green' if node == ev_node else 'red' if node.startswith('CStations') else 'yellow' if node in shortest_path else 'purple' if node.startswith('EVehicles') else 'blue' for node in roadMap.nodes()]
                nx.draw(roadMap, pos, with_labels=True, node_size=500, node_color=node_colors, font_size=8, edge_color='black', width=2.5, alpha=1.0)
                plt.title('Bipartite Graph for Shortest Path to Closest Charging Station')
                plt.show()
                
                break
            else:
                print("No valid path found. Regenerating the graph...")
        else:
            print(f"Invalid input. Please enter a number between 1 and {num_evs}.")
elif calculate_option == '2':
    num_cases = 5
    num_evs_list = []
    energy_spent_avg_list = []
    total_distance_avg_list = []

    for i in range(num_cases):
        num_evs_case = int(input(f"Enter the number of EVs for case {i+1}: "))
        num_evs_list.append(num_evs_case)
        energy_spent_list, total_distance_list = simulate_multiple_evs(roadMap, num_evs_case, energy_consumption_rate)
        energy_spent_avg = sum(energy_spent_list) / len(energy_spent_list) if energy_spent_list else 0
        total_distance_avg = sum(total_distance_list) / len(total_distance_list) if total_distance_list else 0
        energy_spent_avg_list.append(energy_spent_avg)
        total_distance_avg_list.append(total_distance_avg)
        
        # Print average distance for the current case
        print(f"Average total distance for case {i+1}: {total_distance_avg:.2f} km")
        
        # For the first case, also print the shortest distance
        if i == 0:
            shortest_distance = min(total_distance_list) if total_distance_list else 0
            print(f"Shortest total distance for case 1: {shortest_distance:.2f} km")

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(num_evs_list, total_distance_avg_list, marker='o', linestyle='-', color='r')
    plt.xlabel('Number of EVs')
    plt.ylabel('Average Total Distance')
    plt.title('Average Total Distance vs Number of EVs')

    plt.subplot(1, 2, 2)
    plt.plot(num_evs_list, energy_spent_avg_list, marker='o', linestyle='-', color='b')
    plt.xlabel('Number of EVs')
    plt.ylabel('Average Energy Spent')
    plt.title('Average Energy Spent vs Number of EVs')

    plt.tight_layout()
    plt.show() 
