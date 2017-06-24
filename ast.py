from heapq import heappop, heappush, heapify
class State:
    def __init__(self, board, parent = None, move = "", dept = 0):
        self.board = board
        self.parent = parent
        self.move = move
        self.dept = dept
    def generate_next_board(self, dept = 0):
        i = self.board.index(0)
        if i in [3, 4, 5, 6, 7, 8]:
            next_board = self.board[:]
            next_board[i], next_board[i - 3] = next_board[i - 3], next_board[i]
            yield State(next_board, self, "Up", dept)
        if i in [0, 1, 2, 3, 4, 5]:
            next_board = self.board[:]
            next_board[i], next_board[i + 3] = next_board[i + 3], next_board[i]
            yield State(next_board, self, "Down", dept)
        if i in [1, 2, 4, 5, 7, 8]:
            next_board = self.board[:]
            next_board[i], next_board[i - 1] = next_board[i - 1], next_board[i]
            yield State(next_board, self, "Left", dept)                    
        if i in [0, 1, 3, 4, 6, 7]:
            next_board = self.board[:]
            next_board[i], next_board[i + 1] = next_board[i + 1], next_board[i]
            yield State(next_board, self, "Right", dept)

    def __hash__(self):
        return hash(str(self.board))
    def __str__(self):
        string = [str(self.board[i]) + " " + str(self.board[i + 1]) + " " +str(self.board[i + 2]) for i in range(0, 7, 3)]
        return "\n".join(string)
    def mht(self):
        index = self.board.index(0)
        tmp1 = [abs((self.board[i] % 3) - (i % 3)) for i in range(9) if i != index]
        tmp2 = [abs(int(self.board[i] / 3) - int(i / 3)) for i in range(9) if i != index]
        return sum([tmp1[i] + tmp2[i] for i in range(8)])
    def __lt__(self, other):
        return self.mht() < other.mht()
    def __eq__(self, other):
        return self.board == other.board

class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.dict = {}
    def push(self, state, hcost, dept):
        cost = hcost + dept
        heappush(self.heap, (cost, state))
    def pop(self):
        cost, state = heappop(self.heap)
        return state
    def __len__(self):
        return len(self.heap)
    def isEmpty(self):
        return self.__len__() == 0
    
class Solver:
    def __init__(self, board):
        self.state = State(board)
    #    self.goal = State(list(range(9)))
    def _buildPath(self, end):
        path = [end.move]
        state = end.parent
        while state.parent:
            path.append(state.move)
            state = state.parent
        #path.append(self.state.move)    
        return path[:: -1]
    def solve(self):
        goal = list(range(9))
        frontier = PriorityQueue()
        explored = set()
        dept = 0
        max_dept = 0
        node_expand = 0
        frontier.push(self.state, self.state.mht(), dept)
        while not frontier.isEmpty():
            state = frontier.pop()
            node_expand += 1
            explored.add(state)
            if state.board == goal:
                path = self._buildPath(state)
                return path, state.dept, node_expand
            if state.dept == max_dept:
                max_dept += 1
            for x in state.generate_next_board(state.dept + 1):
                if x not in explored:
                    frontier.push(x, x.mht(), x.dept)
        path = []
        return path 
if __name__ == "__main__":
    initState = [8,6,4,2,1,3,5,7,0]
    # print("Initial state:")
    # print(initState)
    # print("Mahatan distance:", initState.mht())
    # frontier = PriorityQueue()
    # for x in initState.generate_next_board():
    #     frontier.push(x, x.mht(), x.dept)
    # while not frontier.isEmpty():
    #     x = frontier.pop()
    #     print(x)
    #     print("Mahattan distance: ", x.mht(), "Move:", x.move)
    # print(initState)
    test = Solver(initState)
    path, dept, node_expand  = test.solve()
    # for x in path:
    #     print(x)
    print(path)
    print("Cost:",len(path))
    print("Dept search:", dept)
    print("Node expand:", node_expand)