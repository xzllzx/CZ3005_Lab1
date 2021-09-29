# Use Coord.json for straight-line distance, for A* search
from queue import PriorityQueue
import json
import math
import Task2

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
    q.put((straight_dict(start), 0.0, 0.0, [start]))
    visited = []

    while not q.empty():
        total_est_distance, current_distance, current_cost, path = q.get()
        # Last node in the current path to obtain current node
        current_node = path[-1]

        if current_node not in visited and current_cost <= max_cost:
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
                q.put((updated_distance, updated_cost, updated_path))
    
    print("No paths found between the two nodes.")
    # Return what?
    return False, path, current_distance, current_cost

if __name__ == "__main__":
    Task3_straight_dict = straight_goal_dict('50')
    Task3_dist_cost_dict = Task2.dist_cost_dict()

    path_found, path, dist, cost = constrained_Astar(Task3_straight_dict, Task3_dist_cost_dict, '1', '50', 300000)
    
    '''
    if not path_found:
        path_found, path, dist, cost = min_cost_UCS(Task2_dict, '1', '50', 183000)
    '''

    if path_found:
        path = '->'.join(path)
        print("Shortest path: ", path)
        print("\nShortest distance: ", dist)
        print("Total energy cost: ", cost)
    