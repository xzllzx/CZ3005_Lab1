import json
import Task1, Task2, Task3

# G, Coord contains 264346 nodes
# G is a dictionary with k,v Node: [Neighbour_list]
# Coord is a dictionary with k,v Node: [X, Y]

# Dist, Cost contains 730100 edges
# Dist is a dictionary with k,v Node1, Node2: Distance
# Cost is a dictionary with k,v Node1, Node2: Cost

# Task 1
def Task_1():
    Task1_dict = Task1.distance_dict()
    #print("Enter the 2 nodes")

    # Loop until no KeyError
    while(True):
        #x = input("Start node: ")
        #y = input("End node: ")
        x = '1'
        y = '50'
        try:
            return Task1.UCS(Task1_dict, x, y)
        except KeyError:
            print("Invalid nodes were entered - Please try again.")

if __name__ == "__main__":
    path, total_distance = Task_1()
    path = '->'.join(path)
    print("Shortest path: ", path, "\n\nShortest Distance: ", total_distance)