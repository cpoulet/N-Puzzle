###############################################################################
#            _   _        _____  _    _ _____________      ______             #
#           | \ | |      |  __ \| |  | |___  /___  / |    |  ____|            #
#           |  \| |______| |__) | |  | |  / /   / /| |    | |__               #
#           | . ` |______|  ___/| |  | | / /   / / | |    |  __|              #
#           | |\  |      | |    | |__| |/ /__ / /__| |____| |____             #
#           |_| \_|      |_|     \____//_____/_____|______|______|            #
#                                                                             #
###############################################################################

import time

from orderedvaluedict import OrderedValueDict
from state import State

class AStar:
    def __init__(self, start, stop, size, heuristic):
        self.size = size
        self.start = State(start)
        self.stop = stop
        self._open = OrderedValueDict()
        self._open.push(self.start.key, self.start, self.start.f)
        self._close = {}
        self.state_number = 0
        self.h = heuristic

    def proceed(self):
        print('Solving Puzzle...')
        t = time.time()
        while not self._open.empty():
            self.state_number += 1
            m = self._open.pop()
            if m.state == self.stop:
                return self.printSolution(m, t)
            self._close[m.key] = m.f
            for child in self._get_child(m.state):
                c = State(child, m, self.h)
                k = self._open.get(c.key)
                l = c.key in self._close
                if not k and not l:
                    self._open.push(c.key, c, c.f)
                elif k:
                    if k.f > c.f:
                        self._open.remove(c.key)
                        self._open.push(c.key, c, c.f)
                elif l:
                    if self._close.get(c.key) > c.f:
                        self._close.pop(c.key)
                        self._open.push(c.key, c, c.f)

    def printSolution(self, state, t):
        print ('Success in {:.3f} seconds.'.format(time.time() - t))
        print ('◦ Total number of states ever selected in the opened set:')
        print('  ', self.state_number)
        print ('◦ Maximum number of states ever represented in memory at the same time:')
        print('  ', self._open.lenmax)
        print ('◦ Number of moves required to transition from the initial state to the final state:')
        return state

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
        return [x[0] * size + x[1] for x in [up, left, right, down] if not -1 in x and not size in x]
