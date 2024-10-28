import tracemalloc
import time

# Check apakah equation yang diberikan valid
def isValidEquation(equation):
    parts = equation.upper().split()
    if len(parts) < 3 or parts[-2] != '=':
        return False
    
    operands, operators, result = splitEquation(equation)
    if(any(not operand.isalpha() for operand in operands + [result])):
        return False
    return True

# Split equation into parts
def splitEquation(equation):
    parts = equation.upper().split()
    operands = parts[:-2:2]             # start = 0, stop = -2 (second to last element), step = 2.  
    operators = parts[1:-2:2]
    result = parts[-1]
    return operands, operators, result

# Mendapatkan huruf unik dari equation
def extractUniqueLetters(equation):
    operands, _, result = splitEquation(equation)
    return [i for i in set(''.join(operands) + result) if i.isalpha()]

# Mendapatkan huruf pertama dari setiap kata
def startingLetters(equation, letters):
    operands, _, result = splitEquation(equation)
    words = operands + [result]
    return [letters[i] for i in range(len(letters)) if letters[i] in [word[0] for word in words if word.isalpha()]]

# Mengubah kata menjadi angka berdasarkan assignment
def wordToNumber(word, assignment):
    return int(''.join(str(assignment[letter]) for letter in word))

def evaluateWithPrecedence(operand_numbers, operators):
    i = 0
    while i < len(operators):
        if operators[i] in '*/':
            if operators[i] == '*':
                operand_numbers[i] *= operand_numbers[i + 1]
            elif operators[i] == '/':
                if operand_numbers[i + 1] == 0:
                    return None
                operand_numbers[i] /= operand_numbers[i + 1]
            del operand_numbers[i + 1]
            del operators[i]
        else:
            i += 1
    result = operand_numbers[0]
    for i, op in enumerate(operators):
        if op == '+':
            result += operand_numbers[i + 1]
        elif op == '-':
            result -= operand_numbers[i + 1]
    return result


# Cek apakah assignment valid
def validateValues(assignment, equation):
    operands, operators, result = splitEquation(equation)
    if any(assignment[operand[0]] == 0 for operand in operands + [result]):
        return False
    if all(letter in assignment or not letter.isalpha() for letter in ''.join(operands) + result):
        operand_numbers = [wordToNumber(operand, assignment) for operand in operands]
        final_result = wordToNumber(result, assignment)
        calculated_result = evaluateWithPrecedence(operand_numbers, operators)
        return calculated_result == final_result
    return False

# SELECT-UNASSIGNED-VARIABLE
def selectUnassignedVariable(assignment, letters, domains):
    unassigned = [v for v in letters if v not in assignment]
    if not unassigned:
        return None
    
    # Minimum Remaining Values
    unassigned.sort(key=lambda var: len(domains[var]))

    # Most Constraining Variable, jika ada 1 atau lebih variabel dengan nilai MRV yang sama
    least_mrv_vars = [
        var for var in unassigned 
        if len(domains[var]) == len(domains[unassigned[0]])
    ]
    
    # Hitung degree dari setiap variabel di least_mrv_vars
    degrees = [
        len([v for v in unassigned if v != var]) 
        for var in least_mrv_vars
    ]
    maxDegree = max(degrees)

    for var in unassigned:
        connections = len([v for v in unassigned if v != var])
        if connections == maxDegree:
            selected_var = var
    return selected_var

# Backtracking search
def backtrack(assignment, variables, domains, equation):
    if len(assignment) == len(variables):
        if validateValues(assignment, equation):
            return assignment
        else:
            return None
    var = selectUnassignedVariable(assignment, variables, domains)
    for value in domains[var]:
        if value not in assignment.values():
            # CONSTRAINT: Huruf pertama dari setiap kata tidak boleh bernilai 0
            if var in startingLetters(equation, variables) and value == '0':
                continue
            assignment[var] = value
            result = backtrack(assignment, variables, domains, equation)
            if result:
                return result
            del assignment[var]
        
    # No solution
    return None

def solveCSP(equation):
    if not isValidEquation(equation):
        print("Invalid input format. Check your input format\n")
        return
    variables = extractUniqueLetters(equation)

    # CONSTRAINT: Jumlah huruf unik dalam problem tidak boleh lebih dari 10
    if len(variables) > 10:
        print("INVALID: The problem cannot contain more than 10 unique letters.\n")
        return
    assignment = {}

    # Inisialisasi domain
    domains = {var: list('0123456789') for var in variables}
    print("\nCSP INITIAL INFORMATION")
    print(f"CSP Variables: {variables}")
    print("Domain CSP:")
    for var in variables:
        print(f"{var}: {domains[var]}")
    print("\nSearching for solution...\n")

    # Backtracking search
    assignment = backtrack(assignment, variables, domains, equation)
    print("SOLUTION RESULT")
    print("Entered equation:", equation)

    # Jika ada complete assignment yang memenuhi semua constraint
    if assignment:
        print(f"Solution found with assignment: {assignment}")
        operands, operators, result = splitEquation(equation)
        print(f"Final result: ", end='')
        for i in range(len(operators)):
            print(f"{wordToNumber(operands[i], assignment)} {operators[i]}", end=' ')
        print(f"{wordToNumber(operands[-1], assignment)} = {wordToNumber(result, assignment)}")
        print()

    # Tidak ada solusi valid yang ditemukan
    else:
        print("No valid solution found.\n")

problem = input("Enter the equation (example: A + B * C = D): ")

if problem:
    tracemalloc.start()
    start_time = time.time()
    solveCSP(problem)
    end_time = time.time()
    memory_usage, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"Runtime : {end_time - start_time: .4f} seconds")
    print(f"Memory Usage : {memory_usage / 1024: .2f} KB")
