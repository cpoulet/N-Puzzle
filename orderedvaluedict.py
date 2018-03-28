###############################################################################
#            _   _        _____  _    _ _____________      ______             #
#           | \ | |      |  __ \| |  | |___  /___  / |    |  ____|            #
#           |  \| |______| |__) | |  | |  / /   / /| |    | |__               #
#           | . ` |______|  ___/| |  | | / /   / / | |    |  __|              #
#           | |\  |      | |    | |__| |/ /__ / /__| |____| |____             #
#           |_| \_|      |_|     \____//_____/_____|______|______|            #
#                                                                             #
###############################################################################

import heapq

class OrderedValueDict:
    '''Sorted Dictionnary with:
    O(1) :      pop()
                contain()
    O(log(n)) : insort()'''
    def __init__(self):
        self._d = {}
        self._queue = []
        self.lenmax = 0

    def push(self, key, value, sort_val):
        self._d[key] = value
        heapq.heappush(self._queue, (sort_val, key))
        if len(self._queue) > self.lenmax:
            self.lenmax += 1

    def __contains__(self, key):
        return key in self._d

    def get(self, key):
        return self._d.get(key)

    def pop(self):
        _, key = heapq.heappop(self._queue)
        return self._d.pop(key)

    def remove(self, key):
        state = self._d.pop(key)
        self._queue.remove((state.f, key))

    def empty(self):
        return not len(self._queue)
