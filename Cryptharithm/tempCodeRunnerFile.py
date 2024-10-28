import tracemalloc
import time

# Split equation menjadi tuple
def splitEquation(equation):
    return tuple(equation.upper().split())

# Mendapatkan huruf unik dari equation
def extractUniqueLetters(equation):
    return [i for i in set(''.join(splitEquation(equation))) if i.isalpha()]

# Mendapatkan huruf pertama dari setiap kata
def startingLetters(equation, letters):
    parts = splitEquation(equation)
    return [letters[i] for i in range(len(letters)) if letters[i] in [part[0] for part in parts if part.isalpha()]]

# Mengubah kata menjadi angka berdasarkan assignment
def wordToNumber(word, assignment):
    return int(''.join(str(assignment[letter]) for letter in word))

# Cek apakah assignment valid
def validateValues(assignment, equation):
    operand1, operator, operand2, equals, result = splitEquation(equation)
    
    # Jika semua huruf dalam operand1, operand2, dan result sudah di-assign
    if all(letter in assignment or not letter.isalpha() for letter in operand1 + operand2 + result):
        num1 = wordToNumber(operand1, assignment)
        num2 = wordToNumber(operand2, assignment)
        finalRes = wordToNumber(result, assignment)

        if operator == '+':
            return num1 + num2 == finalRes
        elif operator == '-':
            return num1 - num2 == finalRes
        elif operator == '*':
            return num1 * num2 == finalRes
        elif operator == '/':
            return num2 != 0 and num1 / num2 == finalRes
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
            # CONSTRAINT: Angka pertama dari setiap kata tidak boleh bernilai 0
            if var in startingLetters(equation, variables) and value == '0':
                continue
            assignment[var] = value
            
            result = backtrack(assignment, variables, domains, equation)
            if result:
                return result
            del assignment[var]
    
    # Tidak ada solusi
    return None

def solveCSP(equation):
    variables = extractUniqueLetters(equation)

    # CONSTRAINT: Jumlah huruf unik dalam problem tidak boleh lebih dari 10
    if len(variables) > 10:
        print("INVALID: Problem hanya boleh mengandung maksimal 10 huruf yang unik.\n")
        return
    operand1, operator, operand2, equal, result = splitEquation(equation)

    assignment = {}

    # Inisialisasi domain
    domains = {var: list('0123456789') for var in variables}

    print("\nINFORMASI AWAL CSP")
    print(f"Variabel CSP: {variables}")
    print("Domain CSP:")
    for var in variables:
        print(f"{var}: {domains[var]}")

    print("\nProses pencarian solusi...\n")

    # Backtracking search
    assignment = backtrack(assignment, variables, domains, equation)

    print("HASIL SOLUSI")
    print("Persamaan yang diinputkan:", equation)

    # Jika ada complete assignment yang memenuhi semua constraint
    if assignment:
        print(f"Solusi ditemukan dengan assignment: {assignment}")
        print(f"Hasil akhir: {wordToNumber(operand1, assignment)} {operator} {wordToNumber(operand2, assignment)} = {wordToNumber(result, assignment)}\n")
    
    # Tidak ada solusi valid yang ditemukan
    else:
        print("Tidak ada solusi yang ditemukan.\n")

# Meminta persamaan lengkap dari pengguna
problem = input("Masukkan persamaan (contoh: A + B = C): ")

if problem:
    tracemalloc.start()
    start_time = time.time()
    solveCSP(problem)
    end_time = time.time()
    memory_usage, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"Runtime : {end_time - start_time: .4f} seconds")
    print(f"Memory Usage : {memory_usage / 1024: .2f} KB")
