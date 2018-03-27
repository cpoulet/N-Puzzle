import heapq

from state import State

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._set   = set()
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._set.add(item)
        self._index += 1

    def pop(self):
        _, item = heapq.heappop(self._queue)
        self._set.remove(item)
        self._index -= 1
        return item

    def contain(item):
        return item in self._set

    def remove(item):
        self._set.remove(item)
        for i, elem in self._queue:
            if elem[1] is item:
                del self._queue[i]
                self._index -= 1
                return
