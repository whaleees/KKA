import os
import psutil
import time
from state import State  # Importing the State class, which represents the game state (player, boxes, etc.)
from move import Up, Down, Left, Right  # Importing the move classes to represent movement in the puzzle

# Decorator to count the number of search calls
def counted(f):
    def wrapped(*args, **kwargs):
        wrapped.calls += 1  # Increment the call count each time the function is called
        return f(*args, **kwargs)
    wrapped.calls = 0  # Initialize the call counter to 0
    return wrapped

# Class representing the puzzle
class MyPuzzle:
    def __init__(self):
        # Initialize the puzzle with walls, player position, box positions, and goal positions
        self.walls = [[0, 1, 0, 1, 0, 0],
                      [0, 1, 0, 1, 1, 1],
                      [1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 1],
                      [1, 1, 1, 0, 1, 0],
                      [0, 0, 1, 0, 1, 0]]
        self.player = (3, 3)  # Initial player position
        self.boxes = [(2, 2), (2, 4), (3, 2), (4, 3)]  # Initial positions of the boxes
        self.goals = [(0, 2), (2, 5), (3, 0), (5, 3)]  # Goal positions where boxes should be placed

# IDA* search function that explores the search space within a given cost bound
@counted  # Use the counted decorator to count the number of times this function is called
def search(path, g, bound, puzzle):
    node = path[-1]  # Get the current state (last state in the path)
    f = g + node.distance(puzzle.goals)  # Calculate the f-cost (g + heuristic distance to the goal)
    
    # If f-cost exceeds the current bound, return failure and the minimum f-cost encountered
    if f > bound:
        return False, f
    
    # If the current state is a goal state, print the path and return success
    if node.success(puzzle.goals):
        # Print the solution (series of moves) by comparing consecutive states in the path
        for state_index in range(1, len(path)):
            if path[state_index-1].player[0] < path[state_index].player[0]:
                print("Down", end=" ")
            elif path[state_index-1].player[0] > path[state_index].player[0]:
                print("Up", end=" ")
            elif path[state_index-1].player[1] < path[state_index].player[1]:
                print("Right", end=" ")
            else:
                print("Left", end=" ")
        return True, bound  # Return success
    
    # Initialize the minimum value for the next bound
    minimum = None
    
    # Define possible moves (Up, Down, Right, Left)
    moves = [Up, Down, Right, Left]
    
    # Try each move from the current state
    for cm in moves:
        m = cm(puzzle.walls)  # Create a move object with the walls as a parameter
        new_state = m.get_state(node)  # Get the new state after applying the move
        
        # If the move is invalid (blocked by walls, etc.), skip it
        if new_state is None:
            continue
        
        # If the new state is not already in the path (to avoid cycles), explore it
        if new_state not in path:
            path.append(new_state)  # Add the new state to the current path
            found, value = search(path, g + 1, bound, puzzle)  # Recursively search from the new state
            
            # If the solution is found, return success
            if found:
                return found, bound
            
            # Update the minimum value for the next bound
            if value is not None and (minimum is None or value < minimum):
                minimum = value
            path.pop(-1)  # Remove the last state after exploring it
    return False, minimum  # Return failure and the minimum f-cost encountered

# Main function that initiates the puzzle search
def main():
    puzzle = MyPuzzle()  # Initialize the puzzle
    state = State(puzzle.player, puzzle.boxes)  # Create the initial game state with player and boxes
    
    # Set the initial bound based on the heuristic distance (multiplied by 2 for back-and-forth movement)
    bound = state.distance(puzzle.goals) * 2
    
    path = [state]  # Initialize the search path with the starting state
    
    # Loop until a solution is found or no further search is possible
    while True:
        found, value = search(path, 0, bound, puzzle)  # Call the IDA* search function
        
        # If a solution is found, print the result and return
        if found:
            print()
            print("search calls:", search.calls)  # Print the number of search calls
            process = psutil.Process(os.getpid())
            print(process.memory_info().rss / (1024 * 1024))  # Print memory usage in megabytes
            return path, bound
        
        # If no solution can be found with the current bound, return "not found"
        if value is None:
            return "not found"
        
        # Update the bound for the next iteration
        bound = value

# Entry point of the script
if __name__ == "__main__":
    start_time = time.time()  # Record the start time
    main()  # Run the main function
    # Print the total time taken to find the solution
    print("--- %s seconds ---" % (time.time() - start_time))
