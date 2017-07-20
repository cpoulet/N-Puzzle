#!/usr/bin/env python3

import sys
import random

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
        print('Enter the size S of the N-Puzzle for a SxS grid : ', end='')
        self.size = int(input())
        self.grid = list(range(self.size**2))
        random.shuffle(self.grid)
        self.show_grid()
        self._is_solvable()

    def _check_grid(self):
        if len(self.grid) != self.size ** 2 or len(self.grid) != len(set(self.grid)):
            raise Exception('Wrong grid')
        if max(self.grid) != (self.size ** 2) - 1 or min(self.grid) != 0:
            raise Exception('Wrong tilde')
        self.show_grid()
        self._is_solvable()

    def _is_solvable(self):
        return True

    def show_grid(self):
        k = self.size
        for x in [self.grid[i*k:(i+1)*k] for i in range(k)]:
            print(*[' '* (3-len(str(n))) + str(n) if n else '   ' for n in x])

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

if __name__ == "__main__":
    try:
	    main(sys.argv)
    except Exception as e:
        if str(e):
            print('Error : ' + str(e))
