#!/usr/bin/env python3

import sys
import bisect
import random
import collections

Node = collections.namedtuple('Node', ['f', 'g', 'h', 'value', 'parent']) 

class sortedList:
    '''Sorted list class'''
    def __init__(self):
        self.list = collections.deque()

    def insort(self, elem):
        bisect.insort(self.list, elem)

    def get(self):
        return self.list.popleft()

    def contain(self, elem):
        for i, e in enumerate(self.list):
            if e == elem:
                return i
        return None

    def min(self):
        return self.list[-1]

    def empty(self):
        return not bool(len(self.list))

class AStar:
    def __init__(self, start, stop, size):
        self.size = size
        self.start = start
        self.stop = stop
        self._open = sortedList()
        self._open.insort(Node(0, 0, 0, start, None))
        self._close = []

    def procede(self):
        while not self._open.empty():
            m = self._open.get()
            self._close.append(m)
            for child in self._get_child(m.value):
                g = m.g + 1
                if child == self.stop:
                    self.solution = Node(g, g, 0, child, m)
                    return
                h = self._wrong_place(child)
                c = Node(g + h, g, h, child, m)
                k = self._open.contain(c)
                if k == None and c not in self._close:
                    self._open.insort(c)
                elif k != -1:
                    if self._open.list[k].f > g + h:
                        self._open.list[k] = c
                elif c in self._close: #not opti
                    self._close.remove(c)
                    self._open.insort(c)

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

    def _wrong_place(self, k):
        return len([1 for x, y in zip(k, self.stop) if x != y])

class NSolver:
    def __init__(self):
        self.size = None

    def parse(self, path):
        with open(path, 'r') as f:
            for l in f:
                l = l.split('#')[0]
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
        self._is_solvable()

    def _check_grid(self):
        if len(self.grid) != self.size ** 2 or len(self.grid) != len(set(self.grid)):
            raise Exception('Wrong grid')
        if max(self.grid) != (self.size ** 2) - 1 or min(self.grid) != 0:
            raise Exception('Wrong tile')
        self.show_grid(self.grid)
        self._is_solvable()

    def _is_solvable(self):     #TODO
        return True

    def show_grid(self, grid):
        k = self.size
        for x in [grid[i*k:(i+1)*k] for i in range(k)]:
            print(*[' '* (3-len(str(n))) + str(n) if n else '   ' for n in x])

    def solve(self):
        print('''Wich heuristique would you like to use :
    [0] - Manhattan distance (taxicab distance)
    [1] - Wrong place tiles
    [2] - Right place tiles''')     #TODO Right/wrong place are the same arent they ?
        AS = AStar(self.grid, list(range(1, self.size ** 2)) + [0], self.size)
        AS.procede()
        self._output(AS.solution)

    def _output(self, node):
        if node.parent != None:
            self._output(node.parent)
        self.show_grid(node.value)
        print()

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
    main(sys.argv)
#    try:
#	    main(sys.argv)
#    except Exception as e:
#        if str(e):
#            print('Error : ' + str(e))
