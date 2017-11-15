###############################################################################
#            _   _        _____  _    _ _____________      ______             #
#           | \ | |      |  __ \| |  | |___  /___  / |    |  ____|            #
#           |  \| |______| |__) | |  | |  / /   / /| |    | |__               #
#           | . ` |______|  ___/| |  | | / /   / / | |    |  __|              #
#           | |\  |      | |    | |__| |/ /__ / /__| |____| |____             #
#           |_| \_|      |_|     \____//_____/_____|______|______|            #
#                                                                             #
###############################################################################

# Our modules
import utils

class State:
    '''N-Puzzle State'''
    def __init__(self, state, parent=None, heuristic=None):
        self.state = state
        self.key = utils.ltok(state)
        self.parent = parent
        self.g = parent.g + 1 if parent else 0
        self.h = heuristic(state) if heuristic else 0
        self.f = self.g + self.h
