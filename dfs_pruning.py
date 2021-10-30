class CheckBinaryConstraint:

    # Check if two variables satisfy the arc consistency
    def satisfied(self, x, x_val, y, y_val) -> bool:
        if x == 'A' and y == 'G': return x_val >= y_val
        if x == 'G' and y == 'A': return y_val >= x_val
        # A < H
        if x == 'A' and y == 'H': return x_val < y_val
        if x == 'H' and y == 'A': return y_val < x_val
        # |F-B| = 1
        if (x == 'B' and y == 'F') or (x == 'F' and y == 'B'): return abs(x_val-y_val) == 1
        # G < H
        if x == 'G' and y == 'H': return x_val < y_val
        if x == 'H' and y == 'G': return y_val < x_val
        # |G-C| = 1
        if (x == 'G' and y == 'C') or (x == 'C' and y == 'G'): return abs(x_val-y_val) == 1
        # |H-C| is even
        if (x == 'H' and y == 'C') or (x == 'C' and y == 'H'): return (abs(x_val-y_val) % 2) == 0
        # H != D
        if (x == 'H' and y == 'D') or (x == 'D' and y == 'H'): return x_val != y_val
        # D >= G
        if x == 'D' and y == 'G': return x_val >= y_val
        if x == 'G' and y == 'D': return y_val >= x_val
        # D != C
        if (x == 'C' and y == 'D') or (x == 'D' and y == 'C'): return x_val != y_val
        # E != C
        if (x == 'E' and y == 'C') or (x == 'C' and y == 'E'): return x_val != y_val
        # E < D-1
        if x == 'E' and y == 'D': return x_val < y_val-1
        if x == 'D' and y == 'E': return y_val < x_val-1
        # E != H-2
        if x == 'E' and y == 'H': return x_val != y_val-2
        if x == 'H' and y == 'E': return y_val != x_val-2
        # G != F
        if (x == 'G' and y == 'F') or (x == 'F' and y == 'G'): return x_val != y_val
        # H != F
        if (x == 'H' and y == 'F') or (x == 'F' and y == 'H'): return x_val != y_val
        # C != F
        if (x == 'F' and y == 'C') or (x == 'C' and y == 'F'): return x_val != y_val
        # D != F
        if (x == 'D' and y == 'F') or (x == 'F' and y == 'D'): return x_val != y_val
        # |E-F| is odd
        if (x == 'E' and y == 'F') or (x == 'F' and y == 'E'): return (abs(x_val - y_val) % 2) != 0
        return True


class CSP:
    def __init__(self, variables, domains) -> None:
        self.variables = variables
        self.domains = domains
        self.check_constraint = CheckBinaryConstraint()
        self.solution = []
        self.n_failures = 0
        self.n_solution = 0

    # Check arc consistency of a given variable and all variables assigned before
    def ifConsistent(self, curr_variable, assigned_before) -> bool:
        for assigned_variable in assigned_before:
            if not self.check_constraint.satisfied(curr_variable, assigned_before[curr_variable],
                                                   assigned_variable, assigned_before[assigned_variable]):
                return False
        return True

    # do DFS with pruning
    def backtracking_search(self, assignment):
        # assignment is complete if every variable is assigned
        if len(assignment) == len(self.variables):
            return assignment

        # get all variables that have not assigned in the assignment
        unassigned = [v for v in self.variables if v not in assignment]

        # get all domain values of the first unassigned variable
        curr_variable = unassigned[0]
        for value in self.domains[curr_variable]:
            local_assignment = assignment.copy()
            local_assignment[curr_variable] = value

            # save the generated search tree in a text file
            tree_file = open('generated_tree.txt', "r")
            lines = tree_file.readlines()
            tree_file.close()
            if len(lines) > 0:
                # generate the search tree and make aligned
                if ("failure" in lines[len(lines) - 1].split()) or ("solution" in lines[len(lines) - 1].split()):
                    if curr_variable == "A":
                        with open('generated_tree.txt', 'a') as f:
                            print(curr_variable + '=' + str(value), end=" ", file=f)
                    if curr_variable == "B":
                        with open('generated_tree.txt', 'a') as f:
                            print('    ' + curr_variable + '=' + str(value), end=" ", file=f)
                    if curr_variable == "C":
                        with open('generated_tree.txt', 'a') as f:
                            print('        ' + curr_variable + '=' + str(value), end=" ", file=f)
                    if curr_variable == "D":
                        with open('generated_tree.txt', 'a') as f:
                            print('            ' + curr_variable + '=' + str(value), end=" ", file=f)
                    if curr_variable == "E":
                        with open('generated_tree.txt', 'a') as f:
                            print('                ' + curr_variable + '=' + str(value), end=" ", file=f)
                    if curr_variable == "F":
                        with open('generated_tree.txt', 'a') as f:
                            print('                    ' + curr_variable + '=' + str(value), end=" ", file=f)
                    if curr_variable == "G":
                        with open('generated_tree.txt', 'a') as f:
                            print('                        ' + curr_variable + '=' + str(value), end=" ", file=f)
                    if curr_variable == "H":
                        with open('generated_tree.txt', 'a') as f:
                            print('                            ' + curr_variable + '=' + str(value), end=" ", file=f)
                else:
                    with open('generated_tree.txt', 'a') as f:
                        print(curr_variable + '=' + str(value), end=" ", file=f)
            else:
                with open('generated_tree.txt', 'a') as f:
                    print(curr_variable + '=' + str(value), end=" ", file=f)

            if not self.ifConsistent(curr_variable, local_assignment):
                self.n_failures = self.n_failures + 1
                with open('generated_tree.txt', 'a') as f:
                    print("failure", file=f)

            if self.ifConsistent(curr_variable, local_assignment):
                result = self.backtracking_search(local_assignment)
                if (result is not None) and (result not in self.solution):
                    self.n_solution = self.n_solution + 1
                    with open('generated_tree.txt', 'a') as f:
                        print("solution", file=f)
                    self.solution.append(result)

        return None

if __name__ == "__main__":
    # initialize variables ordering, can be changed during initialization
    variables = ["A", "B", "C", "D", "E", "F", "G", "H"]
    # variables = ["F", "H", "C", "D", "G", "E", "A", "B"]
    domains = {}
    for variable in variables:
        domains[variable] = [1, 2, 3, 4]
    csp = CSP(variables, domains)
    csp.backtracking_search({})
    solution = csp.solution
    if solution is None:
        print("No solution found")
    else:
        print(solution)
        print(csp.n_solution)
        print(csp.n_failures)
