from itertools import permutations
import time
import tracemalloc

# Function to split equation into components
def splitEquation(equation):
    return tuple(equation.upper().split())

# Function to extract unique letters from the equation
def extractUniqueLetters(equation):
    return [i for i in set(''.join(splitEquation(equation))) if i.isalpha()]

# Function to convert a word to its corresponding number based on a digit assignment
def wordToNumber(word, assignment):
    return int(''.join(str(assignment[letter]) for letter in word))

# Function to validate if the current digit assignment is correct
def validate(equation, assignment):
    operand1, plus, operand2, equals, result = splitEquation(equation)
    
    # Convert the operands and result to numbers based on the current assignment
    num1 = wordToNumber(operand1, assignment)
    num2 = wordToNumber(operand2, assignment)
    sumResult = wordToNumber(result, assignment)
    
    # Check if the sum of the two operands equals the result
    return num1 + num2 == sumResult

# Brute force solver
def bruteForceSolve(equation):
    # Extract unique letters from the equation
    uniqueLetters = extractUniqueLetters(equation)
    
    # Constraint: We can't have more than 10 unique letters since we have only 10 digits
    if len(uniqueLetters) > 10:
        print("INVALID: Too many unique letters.")
        return
    
    # Generate all possible permutations of digits for the unique letters
    for perm in permutations(range(10), len(uniqueLetters)):
        # Create an assignment map (assign digits to letters)
        assignment = dict(zip(uniqueLetters, perm))
        
        # Check if the first letter of any operand or result is assigned 0 (which is invalid)
        operand1, plus, operand2, equals, result = splitEquation(equation)
        if assignment[operand1[0]] == 0 or assignment[operand2[0]] == 0 or assignment[result[0]] == 0:
            continue  # Skip this permutation if a leading letter has a 0 assignment
        
        # Validate the assignment
        if validate(equation, assignment):
            print(f"Solution found: {assignment}")
            print(f"{wordToNumber(operand1, assignment)} + {wordToNumber(operand2, assignment)} = {wordToNumber(result, assignment)}")
            return assignment
    
    # If no solution is found
    print("No solution found.")

# Example usage
equation = "SEND + MORE = MONEY"

tracemalloc.start()
start_time = time.time()
bruteForceSolve(equation)
end_time = time.time()
memory_usage, _ = tracemalloc.get_traced_memory()
tracemalloc.stop()
print(f"\n\nRuntime : {end_time - start_time:.4f} seconds")
print(f"\nMemory Usage : {memory_usage / 1024:.2f} KB")
