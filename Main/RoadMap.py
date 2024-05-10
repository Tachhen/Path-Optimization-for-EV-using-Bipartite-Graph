import networkx as nx
import matplotlib.pyplot as plt
import random

roadMap = nx.Graph()

EVehicles = [f'EVehicles{i}' for i in range(1, 16)]
CStations = [f'CStations{i}' for i in range(1, 5)]
EmtRoads = [f'EmtRoads{i}' for i in range(1, 26)]

roadMap.add_nodes_from(EVehicles, bipartite=0, color='green')  
roadMap.add_nodes_from(EmtRoads, bipartite=1)  
roadMap.add_nodes_from(CStations, bipartite=1, color='red') 
pos = {}
for node in EVehicles + CStations + EmtRoads:
    while True:
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        if all(((x - pos[other_node][0])**2 + (y - pos[other_node][1])**2)**0.5 >= 10 for other_node in pos):
            pos[node] = (x, y)
            break

for node, position in pos.items():
    roadMap.add_node(node, pos=position)


for node in roadMap.nodes():
    if roadMap.nodes[node]['bipartite'] == 0:  
        distances = {other_node: ((pos[node][0] - pos[other_node][0])**2 + (pos[node][1] - pos[other_node][1])**2)**0.5 for other_node in roadMap.nodes() if roadMap.nodes[other_node]['bipartite'] == 1}  
    elif roadMap.nodes[node]['bipartite'] == 1:  
        distances = {other_node: ((pos[node][0] - pos[other_node][0])**2 + (pos[node][1] - pos[other_node][1])**2)**0.5 for other_node in roadMap.nodes() if roadMap.nodes[other_node]['bipartite'] == 0}  
    closest_neighbors = sorted(distances, key=distances.get)[:2]
    roadMap.add_edges_from([(node, neighbor) for neighbor in closest_neighbors])

node_colors = [roadMap.nodes[node].get('color', 'blue') for node in roadMap.nodes()]

plt.figure(figsize=(20, 8))
nx.draw(roadMap, pos, with_labels=False, node_size=300, node_color=node_colors, font_size=8, edge_color='black', width=1.5, alpha=0.7)
plt.show()

