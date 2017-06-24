from heapq import heappop, heappush, heapify
class State:
    def __init__(self, state, dept = 0, parent = None):
        self.state = state
        self.dept = dept
        self.parent = parent
    #heuristic function
    def _h(self):
        sl = [int(abs(self.state[i] - i)) for i in range(9)]

        return sum([int(i % 3) + int(i // 3) for i in sl])
    def _g(self):
        return self.dept
    def __eq__(self, other):
        return self.state == other.state
    def __str__(self):
        string = [str(self.state[i]) + " " + str(self.state[i + 1]) + " " +str(self.state[i + 2]) for i in range(0, 7, 3)]
        return "\n".join(string)
    def __hash__(self):
        return hash(str(self.state))
    def cost(self):
        return self._h() + self._g()
    def __lt__(self, other):
        return self.cost() < other.cost()
    def generate_next_states(self, dept):
        i = self.state.index(0)
        if i in [3, 4, 5, 6, 7, 8]:
            next_state = self.state[:]
            next_state[i], next_state[i - 3] = next_state[i - 3], next_state[i]
            yield State(next_state, dept, self.state)
        if i in [1, 2, 4, 5, 7, 8]:
            next_state = self.state[:]
            next_state[i], next_state[i - 1] = next_state[i - 1], next_state[i]
            yield State(next_state, dept, self.state)
        if i in [0, 1, 3, 4, 6, 7]:
            next_state = self.state[:]
            next_state[i], next_state[i + 1] = next_state[i + 1], next_state[i]
            yield State(next_state, dept, self.state)
        if i in [0, 1, 2, 3, 4, 5]:
            next_state = self.state[:]
            next_state[i], next_state[i + 3] = next_state[i + 3], next_state[i]
            yield State(next_state, dept, self.state) 
class Solver:
    def __init__(self, initState):
        self.initState = State(initState)
        self.goal = list(range(9))
    def _constructPath(self, end):
        path = [end]
        current = end.parent
        while current.parent:
            path.append(current)
            current = current.parent
        return path
    def solve_ast(self):
        frontier = PriorityQueue()
        frontier.push(self.initState, heuristic, 0)
        explored = set()
        dept = 0
        while len(frontier) != 0:
            current = frontier.pop()
            explored.add(current)
            if current.state[: -1] == self.goal:
                path = self._constructPath(current)
                return path[:: -1]
            dept += 1
            for tmpstate in current.generate_next_states(dept):
                    if tmpstate not in explored:
                        frontier.push(tmpstate, heuristic, dept)
        path = []
        return path
def heuristic(state):
    sl = [int(abs(state.state[i] - i)) for i in range(9)]
    return sum([int(i % 3) + int(i // 3) for i in sl])    
class PriorityQueue:
    def __init__(self):
        self.heap = []
    def push(self, state, heuristic, dept):
        key = heuristic(state) + dept
        heappush(self.heap, (key, state))
    def pop(self):
        if self.heap:
            key, state = heappop(self.heap)
            return state
    def __len__(self):
        return len(self.heap)
    
    
