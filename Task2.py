from queue import PriorityQueue
import json

'''
Reads json data and returns it as a nested dictionary of {node: {neighbour: weight}}
'''
def dist_cost_dict():
    dist_cost_dict = {}

    with open('G.json','r') as json_file:
        neighbour_dict = json.load(json_file)

    with open('Dist.json','r') as json_file:
        dist_dict = json.load(json_file)    

    with open('Cost.json','r') as json_file:
        cost_dict = json.load(json_file)    

    for node in neighbour_dict:
        # Initialises temporary dictionary for current node
        temp_dict = {}

        for neighbour in neighbour_dict[node]:
            # Obtains corresponding distance and cost value for node-neighbour pair from dist_dict
            pair = ','.join((node,neighbour))
            try:
                dist = dist_dict[pair]
                cost = cost_dict[pair]
            except KeyError:
                print("Invalid node pair")
            # Neighbour with its dist and cost as a key-value pair in temp_dict
            temp_dict[neighbour] = dist, cost
        
        # Adds the neighbour-dist pair to nested dictionary dist_cost_dict
        dist_cost_dict[node] = temp_dict

    return dist_cost_dict

'''
Performs a UCS to find the shortest path from a start node to an end node
'''
def UCS(graph_dict, start, end, max_cost):
    # Initialisation
    start = str(start)
    end = str(end)
    # Use PriorityQueue to select the next node with the shortest total distance for expansion
    q = PriorityQueue()
    q.put((0, 0, [start]))
    visited = []

    while not q.empty():
        # IMPORTANT
        # CONSIDER PRIORITISING QUEUE BY CURRENT_COST AND HAVING A MORE LENIENT STOPPING POINT
        # IMPORTANT
        current_distance, current_cost, path = q.get()
        # Last node in the current path to obtain current node
        current_node = path[-1]

        if current_node not in visited:
            visited.append(current_node)

            # Goal state reached
            if current_node == end and current_cost <= max_cost:
                return path, current_distance, current_cost
                break

            # Puts the distance, path into queue
            for new_neighbour in graph_dict[current_node]:
                # Total distance to reach the node from start
                #print(float(graph_dict[current_node][new_neighbour][0]))
                #print(float(graph_dict[current_node][new_neighbour][1]))
                updated_distance = current_distance + float(graph_dict[current_node][new_neighbour][0])
                updated_cost = current_cost + float(graph_dict[current_node][new_neighbour][1])

                # Path to reach the node from start
                updated_path = path.copy()
                updated_path.append(new_neighbour)
                q.put((updated_distance, updated_cost, updated_path))

if __name__ == "__main__":
    test_dict = dist_cost_dict()
    # print(test_dict['1'])
    path, dist, cost = UCS(test_dict, '1', '50', 287932)
    print("Path: ", path)
    print("Dist: ", dist)
    print("Cost: ", cost)
