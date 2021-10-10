import Task1, Task2, Task3
import time

# G, Coord contains 264346 nodes
# G is a dictionary with k,v Node: [Neighbour_list]
# Coord is a dictionary with k,v Node: [X, Y]

# Dist, Cost contains 730100 edges
# Dist is a dictionary with k,v Node1, Node2: Distance
# Cost is a dictionary with k,v Node1, Node2: Cost

if __name__ == "__main__":
    while(True):
        print("\n(1) ------- Task 1: Shortest path with no energy constraints")
        print("(2) ------- Task 2: Uninformed search for shortest path with energy constraints")
        print("(3) ------- Task 3: A* search for shortest path with no energy constraints")
        print("(4) ------- Exit")
        choice = input("Please input your choice: ")
        
        if choice == '4':
            break

        if choice in {'1','2','3'}:
            manual = input("Please enter 1 to use default values from Lab Assignment, or enter 2 to manually input values: ")
            
            if manual == '1':
                start = '1'
                end = '50'
                energy = 287932
            elif manual == '2':
                start = input("Please input the starting node: ")
                end = input("Please input the goal node: ")
                if choice != '1':
                    energy = int(input("Please input the energy budget: "))
            else:
                print("Invalid choice - please try again.")
                continue

        time_start = time.process_time()
        if choice == '1':
            Task1.execute(start, end)
        elif choice == '2':            
            Task2.execute(start, end, energy)
        elif choice == '3':
            Task3.execute(start, end, energy)
        else:
            print("Invalid choice - please try again.")
            continue
        
        print("Time taken for execution: ", time.process_time() - time_start, " seconds")
        done = input("\nPress enter to continue...")
