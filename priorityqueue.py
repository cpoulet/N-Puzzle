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

from state import State

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._d     = {}
        self._index = 0
        self.lenmax = 0

    def push(self, item, key, priority):
        heapq.heappush(self._queue, (priority, self._index, key))
        self._d[key] = item
        self._index += 1
        if (self._index > self.lenmax):
            self.lenmax = self._index

    def pop(self):
        _, _, item = heapq.heappop(self._queue)
        del self._d[item.key]
        self._index -= 1
        return item

    def get(self, key):
        return self._d[key]

    def __contains__(self, key):
        return item.key in self._d

    def remove(self, item):
        del self._d[item]
        for i, elem in ienumerate(self._queue):
            if elem[2] is item:
                del self._queue[i]
                self._index -= 1
                return

    def empty(self):
        return not len(self._queue)
