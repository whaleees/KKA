import os  # For getting process ID to measure memory usage
import psutil  # To measure memory usage
import time  # To track execution time

import queue  # To use a priority queue
from move import Up, Down, Left, Right  # Import movement classes (up, down, left, right)
from node import Node  # Import Node class representing each state of the game
from state import State  # Import State class representing the game configuration

# Optional input function for manual input (currently not used)
def get_input():
    # Input for the grid (walls, boxes, player, and goals)
    walls = []
    for i in range(6):  # Grid size 6x6
        row = input()
        walls.append([int(x) for x in row.split()])  # Convert the input row into a list of integers

    # Input for player's initial position (as a tuple of row and column)
    player = tuple(map(int, input().split()))

    # Input for the number of boxes and their positions
    num_boxes = int(input())
    boxes = [tuple(map(int, input().split())) for _ in range(num_boxes)]

    # Input for the number of goals and their positions
    num_goals = int(input())
    goals = [tuple(map(int, input().split())) for _ in range(num_goals)]

    # Return all the input as a tuple
    return walls, player, boxes, goals

def main():
    # Define the walls grid (1 represents a wall, 0 represents an empty space)
    # walls = [[0, 1, 0, 1, 0, 0],
    #          [0, 1, 0, 1, 1, 1],
    #          [1, 1, 0, 0, 0, 0],
    #          [0, 0, 0, 0, 1, 1],
    #          [1, 1, 1, 0, 1, 0],
    #          [0, 0, 1, 0, 1, 0]]
    
    walls = [[1, 1, 1, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 0, 0, 0, 1],
             [1, 0, 1, 1, 0, 0, 1],
             [1, 0, 1, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 0]]
    
    player = (1, 2)
    boxes = [(1, 3), (2, 4), (3, 4), (5, 4), (5, 1), (5, 3), (5, 5)]
    goals = [(1, 1), (2, 5), (3, 1), (4, 4), (5, 6), (4, 6), (5, 3)]

    # player = (2, 1)
    # boxes = [(3, 1), (4, 2), (4, 3), (4, 5), (1, 5), (3, 5), (5, 5)]
    # goals = [(1, 1), (5, 2), (1, 3), (4, 4), (6, 5), (6, 4), (3, 5)]
    
    # Define the initial position of the player
    # player = (3, 3)
    
    # Define the positions of the boxes
    # boxes = [(2, 2), (2, 4), (3, 2), (4, 3)]
    
    # Define the goal positions
    # goals = [(0, 2), (2, 5), (3, 0), (5, 3)]
    
    # Uncomment the following line if you want to use the get_input() function
    # walls, player, boxes, goals = get_input()

    # Set of visited states to avoid reprocessing the same state multiple times
    visited = set()

    # Priority queue (min-heap) to store nodes (states) based on their priority
    pq = queue.PriorityQueue()

    # Create the initial game state with the player's position and box positions
    state = State(player, boxes)

    # Add the initial state to the priority queue with its priority being the Manhattan distance
    pq.put(Node(None, state, 0, None, state.distance(goals)))

    # Flags and variables for tracking the success state and moves
    success = False
    success_node = None
    success_move = None

    # Main A* search loop
    while not pq.empty():
        # Get the node with the lowest priority (based on f(n) = g(n) + h(n))
        node = pq.get()

        # Skip this state if it has already been visited
        if node.state in visited:
            continue

        # Mark the current state as visited
        visited.add(node.state)

        # List of possible movements (up, down, right, left)
        moves = [Up, Down, Right, Left]

        # Check each possible move from the current state
        success = False  # Reset success flag for this loop
        for cm in moves:
            # Create the move object (e.g., Up(walls))
            m = cm(walls)

            # Get the new state after applying the move
            new_state = m.get_state(node.state)

            # If the move is invalid (results in None), skip this move
            if new_state is None:
                continue

            # Check if the new state is a success (i.e., all boxes are on the goals)
            if new_state.success(goals):
                success = True  # Mark the success flag
                success_node = node  # Store the successful node
                success_move = cm  # Store the move that led to success
                break  # Exit the loop as we found a solution

            # If the new state has already been visited, skip it
            if new_state in visited:
                continue

            # Add the new state to the priority queue
            # Priority is based on f(n) = g(n) + h(n)
            pq.put(Node(cm.__name__, new_state, node.depth + 1, node, node.depth + new_state.distance(goals)))

        # If we found a solution, exit the loop
        if success:
            break

    # If a solution is found, print the results
    if success:
        print("Success")

        # Print the sequence of moves that led to the solution
        success_node.print_actions()
        
        # Print the final successful move
        print(success_move.__name__)

        # Print the number of visited states
        print("Visited states: ", len(visited))

        # Print memory usage in megabytes using psutil
        process = psutil.Process(os.getpid())
        print(process.memory_info().rss / (1024 * 1024))  # Convert bytes to megabytes

if __name__ == "__main__":
    # Record the start time
    start_time = time.time()

    # Run the main function
    main()

    # Print the total execution time
    print("--- %s seconds ---" % (time.time() - start_time))
