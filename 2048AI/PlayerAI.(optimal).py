from random import randint
from BaseAI import BaseAI
from math import log
import Grid
class PlayerAI(BaseAI):
    def __init__(self):
        self.depth = 2
    def evalFunction(self, grid):
        maxValue, index = self.getMaxTileValue(grid)
        manhattan = lambda x, y : sum(abs(i - j) for i, j in zip(x, y))
        corner = [(0, 0), (3, 3), (3, 0), (0, 3)]
        distance = min(manhattan(x, index) for x in corner) 
        return 5 * self.freeCell(grid) + 1.2 * self.monocity(grid) - self.smoothGrid(grid) - 4 * distance + maxValue
    def freeCell(self, grid):
        return len(grid.getAvailableCells())
    def maxValue(self, grid, depth):
        if depth == 0 or len(grid.getAvailableMoves()) == 0:
            return self.evalFunction(grid)
        value = -float('inf')
        for move in grid.getAvailableMoves():
            next_grid = grid.clone()
            next_grid.move(move)
            value = max(value, self.minValue(next_grid, depth))
        return value
    def minValue(self, grid, depth):
        if depth == 0 or len(grid.getAvailableCells()) == 0:
            return self.evalFunction(grid)
        value = float('inf')
        for cell in grid.getAvailableCells():
            if randint(0, 99) < 90:
                tileValue = 2
            else:
                tileValue = 4
            tmpGrid = grid.clone()
            tmpGrid.setCellValue(cell, tileValue)
            next_grid = tmpGrid
            value = min(value, self.maxValue(next_grid, depth - 1))
        return value
    def getMaxTileValue(self, grid):
        size = grid.size
        value = 0
        index = (0, 0)
        for i in range(size):
            for j in range(size):
                if grid.map[i][j] > value:
                    value = grid.map[i][j]
                    index = (i, j)
        return value, index
    def monocity(self, grid):
        score = [0, 0, 0, 0]
        #Up-Down side:
        for x in range(4):
            for i in range(3):
                current = grid.map[x][i]
                if current > 0:
                    current = log(current) / log(2)
                nextCell = grid.map[x][i + 1]
                if nextCell > 0:
                    nextCell = log(nextCell) / log(2)
                if current > nextCell:
                    score[0] += current - nextCell
                else:
                    score[1] += nextCell - current
        #Left-Right side:
        for y in range(4):
            for j in range(3):
                current = grid.map[j][y]
                if current > 0:
                    current = log(current) / log(2)
                nextCell = grid.map[j + 1][y]
                if nextCell > 0:
                    nextCell = log(nextCell) / log(2)
                if current > nextCell:
                    score[2] += current - nextCell
                else:
                    score[3] += nextCell - current
        #return max(score[0], score[1]) + max(score[2], score[3])
        return max(score)
    def smoothGrid(self, grid):
        smooth = 0
        for i in range(4):
            for j in range(4):
                if grid.map[i][j] != 0:
                    value = log(grid.map[i][j]) / log(2)
                    if i + 1 < 4 and grid.map[i + 1][j] != 0:
                        nextValue = log(grid.map[i + 1][j]) / log(2)
                        smooth += abs(value - nextValue)
                    if j + 1 < 4 and grid.map[i][j + 1] != 0:
                        nextValue = log(grid.map[i][j + 1]) / log(2)
                        smooth += abs(value - nextValue)
        return smooth
    def maxValueAlphaBeta(self, grid, depth, alpha, beta):
        moves = grid.getAvailableMoves()
        if depth == 0 or not len(moves):
            return self.evalFunction(grid)
        value = -float('inf')
        for move in moves:
            nextGrid = grid.clone()
            nextGrid.move(move)
            value = max(value, self.minValueAlphaBeta(nextGrid, depth, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value
    def minValueAlphaBeta(self, grid, depth, alpha, beta):
        cells = grid.getAvailableCells()
        if depth == 0 or not len(cells):
            return self.evalFunction(grid)
        value = float('inf')
        for cell in cells:
            nextGrid = grid.clone()
            if randint(0, 99) < 90:
                tileValue = 2
            else:
                tileValue = 4
            nextGrid.setCellValue(cell, tileValue)
            value = min(value, self.maxValueAlphaBeta(nextGrid, depth - 1, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value
    def getMove(self, grid):
        best_score = -float('inf')
        beta = float('inf')
        best_move = None
        for move in grid.getAvailableMoves():
            nextGrid = grid.clone()
            nextGrid.move(move)
            value = self.minValueAlphaBeta(nextGrid, self.depth, best_score, beta)
            if value > best_score:
                best_score = value
                best_move = move
        return best_move
