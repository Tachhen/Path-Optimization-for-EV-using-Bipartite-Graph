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
            return None
    closest_cstation = min(shortest_paths, key=lambda x: len(shortest_paths[x]))
    shortest_path = shortest_paths[closest_cstation]
    total_weight = sum(graph[shortest_path[i]][shortest_path[i+1]]['weight'] for i in range(len(shortest_path)-1))
    return shortest_path, total_weight

while True:
    roadMap = nx.Graph()

    EVehicles = [f'EVehicles{i}' for i in range(1, 16)]
    CStations = [f'CStations{i}' for i in range(1, 5)]
    EmtRoads = [f'EmtRoads{i}' for i in range(1, 26)]

    roadMap.add_nodes_from(EVehicles, bipartite=0)  
    roadMap.add_nodes_from(EmtRoads, bipartite=1)  
    roadMap.add_nodes_from(CStations, bipartite=1) 

    # Set fixed positions for CStations
    cstation_positions = {
        'CStations1': (20, 80),
        'CStations2': (80, 20),
        'CStations3': (80, 80),
        'CStations4': (20, 20)
    }

    # Generate random positions for EVehicles and EmtRoads with minimum distance 10
    pos = {}
    for node in EVehicles + EmtRoads + CStations:
        while True:
            x = random.uniform(0, 100)
            y = random.uniform(0, 100)
            if min_distance((x, y), pos, 10):
                pos[node] = (x, y)
                break

    # Assign positions for CStations
    for station, position in cstation_positions.items():
        pos[station] = position

    for node, position in pos.items():
        roadMap.add_node(node, pos=position)

    for node in roadMap.nodes():
        if roadMap.nodes[node]['bipartite'] == 0:  
            distances = {other_node: distance(pos[node], pos[other_node]) for other_node in roadMap.nodes() if roadMap.nodes[other_node]['bipartite'] == 1}  
        elif roadMap.nodes[node]['bipartite'] == 1:  
            distances = {other_node: distance(pos[node], pos[other_node]) for other_node in roadMap.nodes() if roadMap.nodes[other_node]['bipartite'] == 0}  
        closest_neighbors = sorted(distances, key=distances.get)[:2]
        for neighbor in closest_neighbors:
            weight = random.randint(1, 10)  # Assigning random weights for demonstration
            roadMap.add_edge(node, neighbor, weight=weight)

    # Ensure all nodes are connected
    if nx.number_connected_components(roadMap) == 1:
        break

# Interface for selecting EV vehicle number
while True:
    ev_node_number = input("Enter the EV vehicle number (1-15): ")
    if ev_node_number.isdigit() and 1 <= int(ev_node_number) <= 15:
        ev_node = f'EVehicles{ev_node_number}'
        result = shortest_path_to_cstation(roadMap, ev_node)
        if result:
            shortest_path, total_weight = result
            break
        else:
            print("No valid path found. Regenerating the graph...")
    else:
        print("Invalid input. Please enter a number between 1 and 15.")

# Print the shortest path and total weight
print("Shortest path to the closest CStation:", shortest_path)
print("Total weight of the path:", total_weight)

# Plotting the map with the shortest path to the closest CStation highlighted in green
plt.figure(figsize=(20, 8))
node_colors = ['green' if node == ev_node else 'red' if node.startswith('CStations') else 'purple' if node.startswith('EVehicles') else 'blue' for node in roadMap.nodes()]
nx.draw(roadMap, pos, with_labels=True, node_size=300, node_color=node_colors, font_size=8, edge_color='black', width=1.5, alpha=0.7)
plt.show()

