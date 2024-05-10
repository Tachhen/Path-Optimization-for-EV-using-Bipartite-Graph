import heapq

def dijkstra(graph, start):
    # Initialize distances to all nodes as infinity
    distances = {node: float('inf') for node in graph}
    # Distance from start node to itself is 0
    distances[start] = 0
    # Priority queue to keep track of nodes with their tentative distances
    priority_queue = [(0, start)]
    
    while priority_queue:
        # Pop the node with the smallest tentative distance
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # Check if current distance is larger than known distance
        if current_distance > distances[current_node]:
            continue
        
        # Iterate over neighbors of the current node
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            # If the new distance is smaller than the known distance, update it
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances

# Example graph representation (dictionary of dictionaries)
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

# Example usage
start_node = 'A'
shortest_distances = dijkstra(graph, start_node)
print("Shortest distances from node", start_node + ":")
for node, distance in shortest_distances.items():
    print(f"To node {node}: {distance}")

