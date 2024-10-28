import time
import tracemalloc

# Check apakah equation yang diberikan valid
def isValidEquation(equation):
    parts = equation.upper().split()
    if len(parts) < 3 or parts[-2] != '=':
        return False
    return True

# Split equation menjadi tuple
def splitEquation(equation):
    parts = equation.upper().split()
    operands = parts[:-2:2]
    operator = parts[1]
    result = parts[-1]
    return operands, operator, result

# Mendapatkan huruf unik dari equation
def extractUniqueLetters(equation):
    operands, _, result = splitEquation(equation)
    return [i for i in set(''.join(operands) + result) if i.isalpha()]


# Mengubah kata menjadi angka berdasarkan assignment
def wordToNumber(word, assignment):
    return int(''.join(str(assignment[letter]) for letter in word))

# Function to validate if the current digit assignment is correct
def validateValues(assignment, equation):
    operands, operator, result = splitEquation(equation)
    if any(assignment[operand[0]] == 0 for operand in operands + [result]):
        return False
    if all(letter in assignment or not letter.isalpha() for letter in ''.join(operands) + result):
        operand_numbers = [wordToNumber(operand, assignment) for operand in operands]
        final_result = wordToNumber(result, assignment)
        calculated_result = operand_numbers[0]
        for num in operand_numbers[1:]:
            if operator == '+':
                calculated_result += num
            elif operator == '-':
                calculated_result -= num
            elif operator == '*':
                calculated_result *= num
            elif operator == '/':
                if num == 0:
                    return False
                calculated_result /= num
        return calculated_result == final_result
    return False

def recursiveAssignment(depth, max_depth, currentTuple, uniqueLetters, equation):
    if depth == max_depth:
        assignment = dict(zip(uniqueLetters, currentTuple))
        if validateValues(assignment, equation):
            return assignment
        return None
    for i in range(10):
        if currentTuple.count(i) < 1:
            result = recursiveAssignment(depth + 1, max_depth, currentTuple + (i,), uniqueLetters, equation)
            if result is not None:
                return result

def solveBruteForce(equation):
     if not isValidEquation(equation):
        print("Invalid equation format. Please follow the format : A + B + C = D\n")
        return
     uniqueLetters = extractUniqueLetters(equation)
     if len(uniqueLetters) > 10:
        print("INVALID: The problem cannot contain more than 10 unique letters.\n")
        return
     print("\nSearching for solution...\n")
     assignment = recursiveAssignment(0, len(uniqueLetters), (), uniqueLetters, equation)
     if assignment:
        operands, operator, result = splitEquation(equation)
        print(f"Solution found: {assignment}")
        operand_values = f" {operator} ".join(str(wordToNumber(operand, assignment)) for operand in operands)
        final_result = wordToNumber(result, assignment)
        print(f"Final result: {operand_values} = {final_result}")
     else:
        print("No valid solution found.")

problem = input("Enter the equation (example: A + B + C = D): ")

if problem:
    tracemalloc.start()
    start_time = time.time()
    solveBruteForce(problem)
    end_time = time.time()
    memory_usage, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"Runtime : {end_time - start_time: .4f} seconds")
    print(f"Memory Usage : {memory_usage / 1024: .2f} KB")