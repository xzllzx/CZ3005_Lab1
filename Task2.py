from queue import PriorityQueue
import json
from copy import deepcopy

'''
Reads json data and returns it as a nested dictionary of {node: {neighbour: dist, cost}}
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
Performs a UCS to find the shortest path from a start node to an end node, within an energy constraint
'''
def constrained_UCS(graph_dict, start, end, max_cost):
    # Initialisation
    start = str(start)
    end = str(end)

    # Use PriorityQueue to select the next node with the shortest total distance for expansion
    q = PriorityQueue()

    # q is formatted as (distance, energy cost, path)
    q.put((0.0, 0.0, [start]))
    visited = []

    while not q.empty():
        current_distance, current_cost, path = q.get()
        # Last node in the current path to obtain current node
        current_node = path[-1]

        # Goal state reached
        if current_node == end:
            if current_cost <= max_cost:
                return True, True, path, current_distance, current_cost
            else:
                return False, True, path, current_distance, current_cost

        if current_node not in visited  and current_cost <= max_cost:
            visited.append(current_node)

            # Puts the distance, path into queue
            for new_neighbour in graph_dict[current_node]:
                # Total distance to reach the node from start
                updated_distance = current_distance + float(graph_dict[current_node][new_neighbour][0])
                updated_cost = current_cost + float(graph_dict[current_node][new_neighbour][1])

                # Path to reach the node from start
                updated_path = path.copy()
                updated_path.append(new_neighbour)
                q.put((updated_distance, updated_cost, updated_path))
    
    # No path found, queue empty
    return False, False, path, current_distance, current_cost

'''
Performs a UCS to find alternate shortest paths from a start node to an end node, within an energy constraint
Currently not working
'''
def constrained_UCS_2(graph_dict, start, end, max_cost):
    # Initialisation
    start = str(start)
    end = str(end)
    # Use PriorityQueue to select the next node with the shortest total distance for expansion
    q = PriorityQueue()
    q.put((0.0, 0.0, [start]))

    # visited modified to dict storing node and shortest known distance to that node as key-value
    # Also stores all distances to the same node for paths that have lower costs but higher distance
    # If a new path has lower distance: Stores as new lowest_distance
    # Else if a new path has lower cost than lowest_distance: Store as an alternate path
    # Else: Do nothing, go next loop
    shortest_distances = {key: float('inf') for key in graph_dict}
    possible_dist_cost = {}

    while not q.empty():
        # IMPORTANT
        # CONSIDER PRIORITISING QUEUE BY CURRENT_COST AND HAVING A MORE LENIENT STOPPING POINT
        # IMPORTANT
        new_entry = False
        current_distance, current_cost, path = q.get()
        # Last node in the current path to obtain current node
        current_node = path[-1]

        '''
        # Initialise nested dictionary if empty for current_node
        if current_node not in possible_dist_cost:
            possible_dist_cost[current_node] = {}
            possible_dist_cost[current_node][current_distance] = current_cost
            new_entry = True            
            #print(possible_dist_cost[current_node])
        else:           
            #print(possible_dist_cost[current_node])
            #print(current_distance,current_cost)
            for dist,cost in possible_dist_cost[current_node].items():
                if current_distance > dist and current_cost > cost:
                    #print("Rejected - both dist and cost are larger")       
                    pass             
                else:
                    possible_dist_cost[current_node][current_distance] = current_cost
                    # Delete outdated entries
                    new_entry = True
                    break
            if new_entry:
                temp_dict_external = deepcopy(possible_dist_cost[current_node])                
                for dist_i,cost_i in possible_dist_cost[current_node].items():
                    temp_dict_internal = {}
                    for dist_j,cost_j in possible_dist_cost[current_node].items():
                        if dist_j > dist_i and cost_j > cost_i:
                            pass
                        else:
                            temp_dict_internal[dist_j] = cost_j
                    if temp_dict_internal != temp_dict_external:
                        temp_dict_external = deepcopy(temp_dict_internal)
                    possible_dist_cost[current_node] = deepcopy(temp_dict_external)
        '''

        '''
        if current_distance <= shortest_distances[current_node]:
            shortest_distances[current_node] = current_distance
            possible_dist_cost[current_node][current_distance] = current_cost
        else:
            if current_cost < possible_dist_cost[current_node][shortest_distances[current_node]]:
                possible_dist_cost[current_node][current_distance] = current_cost
            
            # Do not execute rest of loop if both current_cost and current_dist are greater than shortest_distance's
            # How to change to check: All paths must have either a lower cost than all lower distances
            else:
                continue
        '''
        
        if new_entry and current_cost <= max_cost:
            # Add node to visited list 
            # visited[current_node](current_node)

            # Goal state reached
            if current_node == end:
                return True, path, current_distance, current_cost

            # Puts the distance, path into queue
            for new_neighbour in graph_dict[current_node]:
                # Total distance to reach the node from start
                updated_distance = current_distance + float(graph_dict[current_node][new_neighbour][0])
                updated_cost = current_cost + float(graph_dict[current_node][new_neighbour][1])

                # Path to reach the node from start
                updated_path = path.copy()
                updated_path.append(new_neighbour)
                q.put((updated_distance, updated_cost, updated_path))
    
    print("No paths found between the two nodes.")
    # Return what?
    return False, path, current_distance, current_cost


'''
Performs a UCS to find the cheapest path from a start node to an end node
'''
def min_cost_UCS(graph_dict, start, end, max_distance):
    # Initialisation
    start = str(start)
    end = str(end)
    # Use PriorityQueue to select the next node with the lowest total cost for expansion
    q = PriorityQueue()
    q.put((0, 0, [start]))
    visited = []

    while not q.empty():
        current_cost, current_distance, path = q.get()
        # Last node in the current path to obtain current node
        current_node = path[-1]

        if current_node not in visited  and current_distance <= max_distance:
            visited.append(current_node)

            # Goal state reached
            if current_node == end:
                return True, path, current_distance, current_cost

            # Puts the distance, path into queue
            for new_neighbour in graph_dict[current_node]:
                # Total distance to reach the node from start
                updated_distance = current_distance + float(graph_dict[current_node][new_neighbour][0])
                updated_cost = current_cost + float(graph_dict[current_node][new_neighbour][1])

                # Path to reach the node from start
                updated_path = path.copy()
                updated_path.append(new_neighbour)
                q.put((updated_cost, updated_distance, updated_path))
    
    print("No paths found between the two nodes.")
    # Return what?
    return False, path, current_distance, current_cost


'''
Initial UCS finds an existing path, but it does not meet the energy constraints.
Repeat UCS iteratively - in each iteration, remove a single edge from the shortest path.
'''
def repeat_UCS(path, dist_cost_dict, start, end, max_cost):
    for i in range(1,len(path)):
        try:
            node1 = path[i-1]
            node2 = path[i]
            temp = dist_cost_dict[node1][node2]

            # Delete an edge
            del(dist_cost_dict[node1][node2])

            energy_met, path_found, path, dist, cost = constrained_UCS(dist_cost_dict, start, end, max_cost)

            # Add deleted edge back
            dist_cost_dict[node1][node2] = temp

            if energy_met and path_found:
                return energy_met, path_found, path, dist, cost
            
        except IndexError:
            continue
    
    print("No path meeting the energy constraints exist.")
    return energy_met, path_found, path, dist, cost

def execute(start, end, energy):
    Task2_dict = dist_cost_dict()
    
    energy_met, path_found, path, dist, cost = constrained_UCS(Task2_dict, start, end, energy)    

    # If path not found, repeat constrained_UCS, but remove one edge each loop
    if not energy_met:
        if path_found:
            print("Path found between the two nodes requires too much energy. Continuing search.")
            energy_met, path_found, path, dist, cost = repeat_UCS(path, Task2_dict, start, end, energy)
        else:
            print("No paths found between the node pair.")
    
    if energy_met and path_found:
        print("Shortest path meeting energy constraints found.\n")
        path = '->'.join(path)
        print("Shortest path: ", path)
        print("\nShortest distance: ", dist)
        print("Total energy cost: ", cost)


if __name__ == "__main__":
    execute('1', '50', 287932)