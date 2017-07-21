import sys
class SudokuCSP:
    def __init__(self, st):
        self.board = {}
        self.domain = {}
        current_row = 'A'
        possible_values = list(range(1, 10))
        for i in range(9):
            for j in range(9):
                index = current_row + str(j + 1)
                value = int(st[9 * i + j])
                self.board[index] = value
                if value != 0:
                    self.domain[index] = [self.board[index]]
                else:
                    self.domain[index] = possible_values
            current_row = chr(ord(current_row) + 1)
        self.current_domain = None
        self.variables = self.board.keys()
        self.nb_assigned_vars = 0
    def assign(self, var, value, assignment):
        assignment[var] = value
        self.nb_assigned_vars += 1
    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]
    def generateNeighbors(self, index):
        current_row = index[0]
        current_col = int(index[1])
        row = 'A'
        neighbors = set()
        for i in range(9):
            if i + 1 != current_col:
                nbindex = current_row + str(i + 1)
                neighbors.add(nbindex)
            if ord(current_row) != ord(row):
                nbindex = row + str(current_col)
                neighbors.add(nbindex)
            row = chr(ord(row) + 1)
        #box
        current_row_factor = int((ord(current_row) - ord('A')) % 3)
        current_col_factor = int(current_col % 3)
        if current_row_factor == 0:
            neigbors_row = [chr(ord(current_row) + 1), chr(ord(current_row) + 2)]
        elif current_row_factor == 1:
            neigbors_row = [chr(ord(current_row) - 1), chr(ord(current_row) + 1)]
        else:
            neigbors_row = [chr(ord(current_row) - 1), chr(ord(current_row) - 2)]
        if current_col_factor == 0:
            neighbors_col = [current_col - 1, current_col - 2]
        elif current_col_factor == 1:
            neighbors_col = [current_col + 1, current_col + 2]
        else:
            neighbors_col = [current_col - 1, current_col + 1]
        for row in neigbors_row:
            for col in neighbors_col:
                neighbors.add(row + str(col))
        return neighbors
    def support_remove_domain_value(self):
        if self.current_domain is None:
            self.current_domain = {x : list(self.domain[x]) for x in self.variables}
    def suppose_assigned(self, var, value):
        self.support_remove_domain_value()
        removal = [(var, a) for a in self.current_domain[var] if a != value]
        self.current_domain[var] = [value]
        return removal
    def remove_domain_value(self, var, value, removal):
        self.current_domain[var].remove(value)
        if removal is not None:
            removal.append((var, value))
    def restore(self, removal):
        for var, value in removal:
            self.current_domain[var].append(value)
    def partial_assigned_list(self):
        self.support_remove_domain_value()
        return {x : self.current_domain[x][0] for x in self.variables if len(self.current_domain[x]) == 1}
    def possible_values(self, var):
        return (self.current_domain or self.domain)[var]
    def contraints(self, var1, value1, var2, value2):
        if var2 not in self.generateNeighbors(var1):
            return True
        else:
            return value1 != value2
    def nbconflicts(self, var, value, assignment):
        count = 0
        for var2 in self.generateNeighbors(var):
            if var2 in assignment and not self.contraints(var, value, var2, assignment[var2]):
                count += 1
        return count

def legal_possibles_values(sudoku, var, assignment):
    if sudoku.current_domain:
        return sudoku.current_domain[var]
    else:
        possible = []
        for value in sudoku.domain[var]:
            if sudoku.nbconflicts(var, value, assignment) == 0:
                possible.append(value)
        return possible
def mrv(sudoku, assignment):
    function  = lambda x : len(legal_possibles_values(sudoku, x, assignment))
    return min([x for x in sudoku.variables if x not in assignment], key = function)
def forward_checking(sudoku, var, value, assignment, removal):
    for var2 in sudoku.generateNeighbors(var):
        if var2 not in assignment:
            for value2 in sudoku.current_domain[var2]:
                if not sudoku.contraints(var, value, var2, value2):
                    sudoku.remove_domain_value(var2, value2, removal)
            if not sudoku.current_domain[var2]:
                return False
    return True
def backtracking_search(sudoku):

    def backtrack(assignment):
        if len(assignment) == len(sudoku.variables):
            return assignment
        var = mrv(sudoku, assignment)
        for value in sudoku.possible_values(var):
            if sudoku.nbconflicts(var, value, assignment) == 0:
                sudoku.assign(var, value, assignment)
                removal = sudoku.suppose_assigned(var, value)
                if forward_checking(sudoku, var, value, assignment, removal):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                sudoku.restore(removal)
        sudoku.unassign(var, assignment)
        return None
    result = backtrack({})
    return result
def revise(sudoku, var1, var2, removal):
    revised = False
    if var2 not in sudoku.generateNeighbors(var1):
        return revised
    for value1 in sudoku.current_domain[var1]:
        satisfy = False
        for value2 in sudoku.current_domain[var2]:
            if value1 != value2:
                satisfy = True
                break
        if not satisfy:
            sudoku.remove_domain_value(var1, value1, removal)
            revised = True
    return revised
def AC3(sudoku):
    removal = []
    queue = [(x, y) for x in sudoku.variables for y in sudoku.generateNeighbors(x)]
    sudoku.support_remove_domain_value()
    while len(queue) > 0:
        var1, var2 = queue.pop()
        if revise(sudoku, var1, var2, removal):
            if not sudoku.current_domain[var1]:
                return False
            for var in sudoku.generateNeighbors(var1):
                if var != var2:
                    queue.append((var, var1))
    assignment = {}
    for var in sudoku.variables:
        if len(sudoku.current_domain[var]) == 1:
            assignment[var] = sudoku.current_domain[var][0]
    return assignment
def isSolved(assignment):
    if len(assignment) == 81:
        return True
    else:
        return False
def result_string(assignment):
    st = ''
    for var in sorted(assignment.keys()):
        st += str(assignment[var])
    return st
if __name__ == "__main__":
    if len(sys.argv) > 1:
        sudoku = SudokuCSP(sys.argv[1])
        assignment = AC3(sudoku)
        if isSolved(assignment):
            st = result_string(assignment) + ' AC3'
        else:
            assignment = backtracking_search(sudoku)
            st = result_string(assignment) + ' BTS'
        f = open('output.txt', 'w')
        f.write(st)
        f.close()