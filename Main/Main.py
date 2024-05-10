import networkx as nx
import matplotlib.pyplot as plt
import random
import math 

def distance(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1]**2))

def min_distance(p,pos,min_distance):
    for pos in pos.values():
        if distance(p,pos)<min_dist:
            return False
        return True

while True:
    calculate=input("Choose an option:\n1.Calculating the shortest path from an EV to the Nearest Charging Station.\n2.Calculating the average distance and energy spent")
    if  calculate in ['1','2']:
        break
    else:
        print("Invalid Option")

while True:
    num_ev=input( "Enter the number of EVs on the road" )
    num_ev=int(num_ev)
roadmap=nx.Graph()
EVehicles=[f'Evehicles{i}' for i  in  range(1,num_ev+1)]
CStations=[f'CStations{i}' for i in range[1,5]]
EmtRoads=[f'EmtRoads{i}' for i in range[1,25]]
roadmap.add_nodes_from(EVehicles,bipartite=0)
roadmap.add_nodes_from(CStations,bipartite=1)
roadmap.add_nodes_from(EmtRoads,bipartite=1)


cstation_positions={
        'CStations1':( 20,80 ),
        'CStations2':(80,20),
        'CStations3':( 80,80 ),
        'CStations4':(20,20)
        }

pos={}
for node in EVehicles+EmtRoads+CStations:
    while True:
        x=random.uniform(0,100)
        y=random.uniform(0,100)
        if min_dis((x,y),pos,10):
            pos[node]=(x,y)
            break

for node in roadMap.nodes():
    if roadMap.nodes[node]['bipartite'] == 0:  
        distances = {other_node: distance(pos[node], pos[other_node]) for other_node in roadMap.nodes() if roadMap.nodes[other_node]['bipartite'] == 1 and node != other_node}  
    elif roadMap.nodes[node]['bipartite'] == 1:  
        distances = {other_node: distance(pos[node], pos[other_node]) for other_node in roadMap.nodes() if roadMap.nodes[other_node]['bipartite'] == 0 and node != other_node}  
    closest_neighbors = sorted(distances, key=distances.get)[:2]
    for neighbor in closest_neighbors:
        weight = random.randint(1, 10)  
        roadMap.add_edge(node, neighbor, weight=weight)

