# Use Coord.json for straight-line distance, for A* search
from queue import PriorityQueue
import json
import math
import Task2
from copy import deepcopy

'''
Reads json data and returns it as a dictionary of {node: straight_line_distance}
'''
def straight_goal_dict(end_node):
    straight_goal_dict = {}

    with open('Coord.json','r') as json_file:
        coord_dict = json.load(json_file)    

    x1, y1 = coord_dict[end_node]

    for node in coord_dict:
        # Initialises temporary dictionary for current node
        x2, y2 = coord_dict[node]

        # Obtains straight line distance from node to each neighbour
        straight_line_dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        # Adds the node and straight line distance to end node as key-value pair to dictionary straight_goal_dict
        straight_goal_dict[node] = straight_line_dist

    return straight_goal_dict

'''
Performs an A* search to find the shortest path from a start node to an end node, within an energy constraint
'''
def constrained_Astar(straight_dict, dist_cost_dict, start, end, max_cost):
    # A* uses f(n) = g(n) + h(n)
    # g(n) = Actual cost to current node from start
    # h(n) = Estimated cost from current node to goal (straight-line distance)
    
    # Initialisation
    start = str(start)
    end = str(end)

    # Use PriorityQueue to select the next node with the shortest total distance for expansion
    q = PriorityQueue()
    
    # q is formatted as (total_estimated_distance, current_actual_distance, energy_cost, path)
    q.put((straight_dict[start], 0.0, 0.0, [start]))
    visited = []

    while not q.empty():
        total_est_distance, current_distance, current_cost, path = q.get()
        # Last node in the current path to obtain current node
        current_node = path[-1]

        # Goal state reached
        if current_node == end:
            if current_cost <= max_cost:
                return True, True, path, current_distance, current_cost
            else:
                return False, True, path, current_distance, current_cost

        if current_node not in visited:
            visited.append(current_node)

            # Puts the distance, path into queue
            for new_neighbour in dist_cost_dict[current_node]:
                # Total distance to reach the node from start
                updated_distance = current_distance + float(dist_cost_dict[current_node][new_neighbour][0])
                updated_cost = current_cost + float(dist_cost_dict[current_node][new_neighbour][1])
                updated_total_est_distance = updated_distance + straight_dict[new_neighbour]

                # Path to reach the node from start
                updated_path = path.copy()
                updated_path.append(new_neighbour)
                q.put((updated_total_est_distance, updated_distance, updated_cost, updated_path))

    # No path found, queue empty
    return False, False, path, current_distance, current_cost

'''
Initial A* search finds an existing path, but it does not meet the energy constraints.
Repeat A* search iteratively - in each iteration, remove a single edge from the shortest path.
'''
def repeat_Astar(path, straight_dict, dist_cost_dict, start, end, max_cost):
    for i in range(1,len(path)):
        try:
            node1 = path[i-1]
            node2 = path[i]
            temp = dist_cost_dict[node1][node2]

            # Delete an edge
            del(dist_cost_dict[node1][node2])

            energy_met, path_found, path, dist, cost = constrained_Astar(straight_dict, dist_cost_dict, start, end, max_cost)

            # Add deleted edge back
            dist_cost_dict[node1][node2] = temp

            if energy_met and path_found:
                return energy_met, path_found, path, dist, cost
        except IndexError:
            continue
    
    print("No path meeting the energy constraints exist.")
    return energy_met, path_found, path, dist, cost

def execute(start, end, energy):
    Task3_straight_dict = straight_goal_dict(end)
    Task3_dist_cost_dict = Task2.dist_cost_dict()

    energy_met, path_found, path, dist, cost = constrained_Astar(Task3_straight_dict, Task3_dist_cost_dict, start, end, energy)
    
    # If path not found, repeat constrained_Astar, but remove one edge each loop
    if not energy_met:
        if path_found:
            print("Path found between the two nodes requires too much energy. Continuing search.")
            energy_met, path_found, path, dist, cost = repeat_Astar(path, Task3_straight_dict, Task3_dist_cost_dict, start, end, energy)
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
    