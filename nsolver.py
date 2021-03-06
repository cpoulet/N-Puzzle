###############################################################################
#            _   _        _____  _    _ _____________      ______             #
#           | \ | |      |  __ \| |  | |___  /___  / |    |  ____|            #
#           |  \| |______| |__) | |  | |  / /   / /| |    | |__               #
#           | . ` |______|  ___/| |  | | / /   / / | |    |  __|              #
#           | |\  |      | |    | |__| |/ /__ / /__| |____| |____             #
#           |_| \_|      |_|     \____//_____/_____|______|______|            #
#                                                                             #
###############################################################################

import os
import re
import time
import random

import utils
import heuristics
from astar import AStar
from generate import makePuzzle

class NSolver:
    def __init__(self, quiet, greedy, uniformcost, visual):
        self.size = None
        self.seq = []
        self.quiet = quiet
        self.greedy = greedy
        self.uc = uniformcost
        self.visual = visual
        self.HEURISTIC = [ heuristics.manhattan, heuristics.missplaced, heuristics.linearconflict, heuristics.euclidiandistance ]

    def parse(self, path):
        with open(path, 'r') as f:
            for l in f:
                l = re.sub(r'\n', '', l.split('#')[0])
                if not l:
                    continue
                if self.size == None:
                    self.size = int(l.strip())
                    self.grid = []
                else:
                    li = l.split()
                    if len(li) != self.size:
                        raise Exception('Wrong grid')
                    self.grid += [int(x) for x in li]
        self._check_grid()

    def generate(self):
        while 1:
            print('Enter the size N of the N-Puzzle for a N * N grid : ', end='')
            self.size = int(input())
            if self.size < 2:
                print("Can't generate a puzzle with size lower than 2, sorry :)")
            elif self.size > 6:
                print("That will be too big for me, sorry :)")
            else:
                break
        self.grid = makePuzzle(self.size)
        self.show_grid(self.grid)

    def _check_grid(self):
        if len(self.grid) != self.size ** 2 or len(self.grid) != len(set(self.grid)):
            raise Exception('Wrong grid')
        if max(self.grid) != (self.size ** 2) - 1 or min(self.grid) != 0:
            raise Exception('Wrong tile')
        self.show_grid(self.grid)
        if not self.is_solvable(self.grid[::]):
            raise Exception('This grid is not solvable.')

    def is_solvable(self, grid):
        s = utils.sqrt[len(grid)]
        aim = utils.snake[s]
        z = sum([abs(x - y) for x, y in zip(utils.pos(grid.index(0), s), utils.pos(aim.index(0), s))]) % 2
        t = 0
        for i in range(len(grid)):
            if grid[i] == aim[i]:
                continue
            else:
                grid[grid.index(aim[i])] = grid[i]
                grid[i] = aim[i]
                t = 1 - t
        return z == t

    def show_grid(self, grid, locate=False):
        k = self.size
        y = 0
        for x in [grid[i * k : (i + 1) * k] for i in range(k)]:
            s = "".join([' ' * (3 - len(str(n))) + str(n) if n else '   ' for n in x])
            if not locate:
                print(s)
            else:
                utils.locate(s, 1, 13 + y + k)
                y += 1
        if locate:
            time.sleep(.200)


    def solve(self):
        print('''Which heuristic would you like to use :
    [0] - Manhattan distance (taxicab distance)
    [1] - Missplaced tiles
    [2] - Linear Conflict
    [3] - Euclidian Distance''')
        try:
            h = self.HEURISTIC[int(input())]
        except IndexError:
            print('Choose a heuristic by entering the corresponding number. thxbye')
            self.solve()
            return
        if self.visual:
            os.system('clear')
            print('Starting grid\n')
            self.show_grid(self.grid)
            print()
        AS = AStar(self.grid, utils.snake[self.size], self.size, h, self.greedy, self.uc)
        self.solution = AS.proceed()
        self._output(self.solution)
        print('  ', len(self.seq))
        if not self.quiet:
            for step in self.seq[::-1]:
                print()
                self.show_grid(step, self.visual)

    def _output(self, state):
        while state.parent != None:
            self.seq.append(state.state)
            state = state.parent
