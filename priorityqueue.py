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

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._d[item] = item
        self._index += 1
        if (self._index > self.lenmax):
            self.lenmax = self._index

    def pop(self):
        _, _, item = heapq.heappop(self._queue)
        del self._d[item]
        self._index -= 1
        return item

    def __contains__(self, item):
        return item in self._d

    def remove(self, item):
        del self._d[item]
        for i, elem in self._queue:
            if elem[2] is item:
                del self._queue[i]
                self._index -= 1
                return

    def empty(self):
        return not len(self._queue)
