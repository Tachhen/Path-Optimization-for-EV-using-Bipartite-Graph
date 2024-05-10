import networkx as nx
import matplotlib.pyplot as plt

my_Graph = nx.Graph()
my_Graph.add_nodes_from(['A1','A2','A3','A4'], bipartite=0)
my_Graph.add_nodes_from(['B1','B2','B3','B4'], bipartite=1)
my_Graph.add_edges_from([('A1', 'B3'), ('A2', 'B2'), ('A3', 'B3'), ('A4', 'B4')])
pos = nx.drawing.layout.bipartite_layout(my_Graph, ['A1', 'A2', 'A3', 'A4'])
nx.draw(my_Graph, pos=pos, node_color=['blue', 'red', 'blue', 'red', 'blue', 'red', 'blue', 'red'])
plt.show()

