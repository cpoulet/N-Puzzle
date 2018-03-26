###############################################################################
#            _   _        _____  _    _ _____________      ______             #
#           | \ | |      |  __ \| |  | |___  /___  / |    |  ____|            #
#           |  \| |______| |__) | |  | |  / /   / /| |    | |__               #
#           | . ` |______|  ___/| |  | | / /   / / | |    |  __|              #
#           | |\  |      | |    | |__| |/ /__ / /__| |____| |____             #
#           |_| \_|      |_|     \____//_____/_____|______|______|            #
#                                                                             #
###############################################################################

import itertools

import utils

def missplaced(state):
    size = utils.sqrt[len(state)]
    return len([x for x, y in zip(state, utils.snake[size]) if x != y])

def manhattan(state):
    d = 0
    size = utils.sqrt[len(state)]
    for i,x in enumerate(state):
        ti = utils.pos(i, size)
        tx = utils.pos(utils.snake[size].index(x), size)
        d += abs(ti[0] - tx[0]) + abs(ti[1] - tx[1])
    return d

def _conflict(li, aim):      #memoization could be usefull
    if li == aim :
        return 0
    union = set(li) & set(aim)
    k = 0
    for x in itertools.permutations(union, 2):
        if li.index(x[0]) > li.index(x[1]) and aim.index(x[0]) < aim.index(x[1]):
            k += 2
    return k

def linearconflict(state):
    size = utils.sqrt[len(state)]
    k = 0
    for i in range(size):
        k += _conflict(state[i*size:(i + 1)*size], utils.snake[size][i*size:(i + 1)*size])
        k += _conflict([state[x*size + i] for x in range(size)],[utils.snake[size][x*size + i] for x in range(size)])
    return k + manhattan(state)
