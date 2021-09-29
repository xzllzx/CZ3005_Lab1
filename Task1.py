from queue import PriorityQueue
import json

'''
Reads json data and returns it as a nested dictionary of {node: {neighbour: weight}}
'''
def distance_dict():
    weighted_dict = {}

    with open('G.json','r') as json_file:
        neighbour_dict = json.load(json_file)

    with open('Dist.json','r') as json_file:
        dist_dict = json.load(json_file)    

    for node in neighbour_dict:
        # Initialises temporary dictionary for current node
        neighbour_weight_dict = {}

        for neighbour in neighbour_dict[node]:
            # Obtains corresponding distance value for node-neighbour pair from dist_dict
            pair = ','.join((node,neighbour))
            try:
                weight = dist_dict[pair]
            except KeyError:
                print("Invalid node pair")
            # Neighbour-weight as a key-value pair in neighbour_weight_dict
            neighbour_weight_dict[neighbour] = weight
        
        # Adds the neighbour-weight pair to nested dictionary weighted_dict
        weighted_dict[node] = neighbour_weight_dict

    return weighted_dict

'''
Performs a UCS to find the shortest path from a start node to an end node
'''
def UCS(graph_dict, start, end):
    # Initialisation
    start = str(start)
    end = str(end)

    # Use PriorityQueue to select the next node with the shortest total distance for expansion
    q = PriorityQueue()

    # q is formatted as (distance, path)
    q.put((0.0, [start]))
    visited = []

    while not q.empty():
        current_distance, path = q.get()
        # Last node in the current path to obtain current node
        current_node = path[-1]

        if current_node not in visited:
            visited.append(current_node)

            # Goal state reached
            if current_node == end:
                return path, current_distance

            # Puts the distance, path into queue
            for new_neighbour in graph_dict[current_node]:
                # Total distance to reach the node from start
                updated_distance = current_distance + float(graph_dict[current_node][new_neighbour])

                # Path to reach the node from start
                updated_path = path.copy()
                updated_path.append(new_neighbour)
                q.put((updated_distance, updated_path))