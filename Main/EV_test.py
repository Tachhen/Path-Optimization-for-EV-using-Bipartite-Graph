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
        return None

while True:
    num_evs = input("Enter the number of EVs on the road: ")
    if num_evs.isdigit() and 1 <= int(num_evs) <= 15:
        num_evs = int(num_evs)
        break
    else:
        print("Invalid input. Please enter a number between 1 and 15.")

while True:
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

    if nx.number_connected_components(roadMap) == 1:
        break

while True:
    ev_node_number = input(f"Enter the EV vehicle number (1-{num_evs}): ")
    if ev_node_number.isdigit() and 1 <= int(ev_node_number) <= num_evs:
        ev_node = f'EVehicles{ev_node_number}'
        result = shortest_path_to_cstation(roadMap, ev_node)
        if result:
            shortest_path, total_weight = result
            break
        else:
            print("No valid path found. Regenerating the graph...")
    else:
        print(f"Invalid input. Please enter a number between 1 and {num_evs}.")

print("Shortest path to the closest CStation:", shortest_path)
print("Total weight of the path:", total_weight)

plt.figure(figsize=(20, 8))
node_colors = ['green' if node == ev_node else 'red' if node.startswith('CStations') else 'yellow' if node in shortest_path else 'purple' if node.startswith('EVehicles') else 'blue' for node in roadMap.nodes()]
nx.draw(roadMap, pos, with_labels=True, node_size=500, node_color=node_colors, font_size=8, edge_color='black', width=2.5, alpha=1.0)
plt.show()

