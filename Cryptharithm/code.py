class CSP_crypt:
    
    def __init__(self, exp):
        p = exp.split()
        self.operands = []
        self.operators = []
        self.state = []
        self.solved = False

        for i, part in enumerate(p):
            if i % 2 == 0:
                self.operands.append(part)
                for q in part:
                    if q not in self.state:
                        self.state.append(q)
            else:
                self.operators.append(part)
        self.result = self.operands[-1]
        self.operands = self.operands[:-1]
        
        for i in range(10 - len(self.state)): 
            self.state.append('x')
    
    def display(self):
        print("Operands:", self.operands)
        print("Operators:", self.operators)
        print("Result:", self.result)
        print("State:", self.state)
        print("Solved:", self.solved)
    
    def display_ans(self):
        for i in self.state:
            if i != 'x':
                print(i, " - ", self.state.index(i))
    
    def apply_constraints(self, depth):
        if len(self.result) >= max(len(op) for op in self.operands):
            if self.state[0] == self.result[0] or self.state[1] == self.result[0]:
                return True
            elif depth < 2:
                return True
        return True

    def get_number(self, p):
        num = 0
        for q in p:
            num = num * 10 + self.state.index(q)
        return num
    
    def solve(self):
        num_result = self.get_number(self.result)
        calculated_result = self.get_number(self.operands[0])

        for i, operator in enumerate(self.operators):
            next_operand = self.get_number(self.operands[i + 1]) if i + 1 < len(self.operands) else calculated_result
            if operator == '+':
                calculated_result += next_operand
            elif operator == '-':
                calculated_result -= next_operand
            elif operator == '*':
                calculated_result *= next_operand
            elif operator == '/':
                if next_operand != 0:  
                    calculated_result /= next_operand
        
        if calculated_result == num_result:
            print("\nCalculated Result =", calculated_result)
            print("Operands:", [self.get_number(op) for op in self.operands])
            print("Result:", num_result)
            self.solved = True
    
    def expand(self, l, r, depth):
        self.solve()
        
        if self.solved:
            return
        elif l == r:
            return
        else:
            for i in range(l, r + 1):
                self.state[l], self.state[i] = self.state[i], self.state[l]
                if self.apply_constraints(depth):
                    depth += 1
                    self.expand(l + 1, r, depth)
                    depth -= 1 
                if self.solved:
                    return
                self.state[i], self.state[l] = self.state[l], self.state[i]

if __name__ == "__main__":
    exp = input("Enter the problem: ")
    c_csp = CSP_crypt(exp)
    
    c_csp.display()
    
    c_csp.expand(0, 9, 0)
    
    c_csp.display()
    
    if c_csp.solved:
        c_csp.display_ans()
