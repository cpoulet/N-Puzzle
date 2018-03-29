###############################################################################
#            _   _        _____  _    _ _____________      ______             #
#           | \ | |      |  __ \| |  | |___  /___  / |    |  ____|            #
#           |  \| |______| |__) | |  | |  / /   / /| |    | |__               #
#           | . ` |______|  ___/| |  | | / /   / / | |    |  __|              #
#           | |\  |      | |    | |__| |/ /__ / /__| |____| |____             #
#           |_| \_|      |_|     \____//_____/_____|______|______|            #
#                                                                             #
###############################################################################

import utils

class State:
    '''N-Puzzle State'''
    def __init__(self, state, parent=None, heuristic=None, greedy=False, uniformcost=False):
        if greedy:
            uniformcost = False
        self.state = state
        self.key = utils.ltok(state)
        self.parent = parent
        self.g = parent.g + 1 if parent and not greedy else 0
        self.h = heuristic(state) if heuristic and not uniformcost else 0
        self.f = self.g + self.h

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

    def __repr__(self):
        return "<STATE key: '{}', f: {}>".format('|'.join([str(x) for x in self.state]), self.f)
