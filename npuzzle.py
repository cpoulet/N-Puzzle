#!/usr/bin/env python3

import re
import sys
import time
import bisect
import random
import collections
from itertools import permutations

snake = {2:[1,2,3,0],
        3:[1,2,3,8,0,4,7,6,5],
        4:[1,2,3,4,12,13,14,5,11,0,15,6,10,9,8,7],
        5:[1,2,3,4,5,16,17,18,19,6,15,24,0,20,7,14,23,22,21,8,13,12,11,10,9]}

sqrt = {4:2,
        9:3,
        16:4,
        25:5}

def pos(nb, size):
    return (nb // size, nb % size)

def missplaced(state):
    size = sqrt[len(state)]
    return len([x for x, y in zip(state, snake[size]) if x != y])

def manhattan(state):
    d = 0
    size = sqrt[len(state)]
    for i,x in enumerate(state):
        ti = pos(i, size)
        tx = pos(snake[size].index(x), size)
        d += abs(ti[0] - tx[0]) + abs(ti[1] - tx[1])
    return d

def conflict(li, aim):      #memoization could be usefull
    if li == aim :
        return 0
    union = set(li) & set(aim)
    k = 0
    for x in permutations(union, 2):
        if li.index(x[0]) > li.index(x[1]) and aim.index(x[0]) < aim.index(x[1]):
            k += 2
    return k

def linearconflict(state):
    size = sqrt[len(state)]
    k = 0
    for i in range(size):
        k += conflict(state[i*size:(i + 1)*size], snake[size][i*size:(i + 1)*size])
        k += conflict([state[x*size + i] for x in range(size)],[snake[size][x*size + i] for x in range(size)])
    return k + manhattan(state)

def ltok(li):
    return ''.join([chr(x) for x in li])

def ktol(key):
    return [ord(x) for x in key]

class State:
    '''N-Puzzle State'''
    def __init__(self, state, parent=None, heuristique=None):
        self.state = state
        self.key = ltok(state)
        self.parent = parent
        self.g = parent.g + 1 if parent else 0
        self.h = heuristique(state) if heuristique else 0
        self.f = self.g + self.h

class OrderedValueDict:
    '''Dictionnary with:
    O(1) :      pop()
                contain()
    O(log(n)) : insort()'''
    def __init__(self):
        self.d = {}
        self.list = collections.deque()
        self.lenmax = 0

    def insort(self, key, value, sort_val):
        self.d[key] = value
        bisect.insort(self.list, (sort_val, key))
        if len(self.list) > self.lenmax:
            self.lenmax += 1

    def contain(self, key):
        return self.d.get(key)

    def pop(self):
        key = self.list.popleft()[1]
        return self.d.pop(key)

    def min(self):
        return self.d[self.list[0][1]]

    def remove(self, key):
        d = self.d.pop(key)
        self.list.remove((d.f, key))

    def empty(self):
        return not len(self.list)

class AStar:
    def __init__(self, start, stop, size, heuristique):
        self.size = size
        self.start = State(start)
        self.stop = stop
        self._open = OrderedValueDict()
        self._open.insort(self.start.key, self.start, self.start.f)
        self._close = {}
        self.state_number = 0
        self.h = heuristique

    def procede(self):
        print('Solving Puzzle...')
        t = time.time()
        while not self._open.empty():
            self.state_number += 1
            m = self._open.pop()
            self._close[m.key] = m.f
            for child in self._get_child(m.state):
                if child == self.stop:
                    print ('Success in {:.3f} seconds.'.format(time.time() - t))
                    print ('◦ Total number of states ever selected in the opened set:')
                    print('  ', self.state_number)
                    print ('◦ Maximum number of states ever represented in memory at the same time:')
                    print('  ', self._open.lenmax)
                    print ('◦ Number of moves required to transition from the initial state to the final state:')
                    return State(child, m)
                c = State(child, m, self.h)
                k = self._open.contain(c.key)
                l = c.key in self._close
                if not k and not l:
                    self._open.insort(c.key, c, c.f)
                elif k:
                    if k.f > c.f:
                        self._open.remove(c.key)
                        self._open.insort(c.key, c, c.f)
                elif l:
                    if self._close.get(c.key) > c.f:
                        self._close.pop(c.key)
                        self._open.insort(c.key, c, c.f)

    def _get_child(self, m):
        z = m.index(0)
        moves = self._side(z, self.size)
        for move in moves:
            child = m.copy()
            child[z], child[move] = child[move], child[z]
            yield child

    def _side(self, nb, size):
        up = (nb // size - 1, nb % size)
        down = (nb // size + 1, nb % size)
        left = (nb // size, nb % size - 1)
        right = (nb // size, nb % size + 1)
        return [x[0]*size + x[1] for x in [up, left, right, down] if not -1 in x and not size in x]

class NSolver:
    def __init__(self):
        self.size = None
        self.seq = []
        self.HEURISTIQUE = [manhattan, missplaced, linearconflict]

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
        print('Enter the size N of the N-Puzzle for a N*N grid : ', end='')
        self.size = int(input())
        if self.size <= 2:
            print('Can\'t generate a puzzle with size lower than 2. Dummy.')
        self.grid = list(range(self.size**2))
        random.shuffle(self.grid)
        self.show_grid()
        if not self.is_solvable(self.grid[::]):
            raise Exception('This grid is not solvable.')

    def _check_grid(self):
        if len(self.grid) != self.size ** 2 or len(self.grid) != len(set(self.grid)):
            raise Exception('Wrong grid')
        if max(self.grid) != (self.size ** 2) - 1 or min(self.grid) != 0:
            raise Exception('Wrong tile')
        self.show_grid(self.grid)
        if not self.is_solvable(self.grid[::]):
            raise Exception('This grid is not solvable.')

    def is_solvable(self, grid):
        s = sqrt[len(grid)]
        aim = snake[s]
        z = sum([abs(x - y) for x, y in zip(pos(grid.index(0), s), pos(aim.index(0), s))]) % 2
        t = 0
        for i in range(len(grid)):
            if grid[i] == aim[i]:
                continue
            else:
                grid[grid.index(aim[i])] = grid[i]
                grid[i] = aim[i]
                t = 1 - t
        return z == t

    def show_grid(self, grid):
        k = self.size
        for x in [grid[i*k:(i+1)*k] for i in range(k)]:
            print(*[' '* (3-len(str(n))) + str(n) if n else '   ' for n in x])

    def solve(self):
        print('''Wich heuristique would you like to use :
    [0] - Manhattan distance (taxicab distance)
    [1] - Missplaced tiles
    [2] - Linear Conflict''')
        try:
            h = self.HEURISTIQUE[int(input())]
        except:
            print('Choose an heuristique by entering the correspondante number. Dummy.')
            self.solve()
            return
        AS = AStar(self.grid, snake[self.size], self.size, h)
        self.solution = AS.procede()
        self._output(self.solution)
        print('  ', len(self.seq))

    def _output(self, state):
        if state.parent != None:
            self._output(state.parent)
        self.seq.append(state.state)

def main(argv):
    if len(argv) > 2:
        print('''usage: ./npuzzle [input_path]

if no input_path are given, a random grid will be generated with a size of users choice''')
        raise Exception('')
    NS = NSolver()
    if len(argv) == 2:
        NS.parse(argv[1].strip())
    else:
        NS.generate()
    NS.solve()

if __name__ == "__main__":
#   main(sys.argv)
    try:
	    main(sys.argv)
    except Exception as e:
        if str(e):
            print('Error : ' + str(e))
