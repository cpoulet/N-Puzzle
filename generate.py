###############################################################################
#            _   _        _____  _    _ _____________      ______             #
#           | \ | |      |  __ \| |  | |___  /___  / |    |  ____|            #
#           |  \| |______| |__) | |  | |  / /   / /| |    | |__               #
#           | . ` |______|  ___/| |  | | / /   / / | |    |  __|              #
#           | |\  |      | |    | |__| |/ /__ / /__| |____| |____             #
#           |_| \_|      |_|     \____//_____/_____|______|______|            #
#                                                                             #
###############################################################################

import sys
import argparse
import random

def makePuzzle(size):
	def swapEmpty(puzzle):
		idx = puzzle.index(0)
		poss = []
		if idx % size > 0:
			poss.append(idx - 1)
		if idx % size < size - 1:
			poss.append(idx + 1)
		if idx / size > 0:
			poss.append(idx - size)
		if idx / size < size - 1:
			poss.append(idx + size)
		swi = random.choice(poss)
		puzzle[idx] = puzzle[swi]
		puzzle[swi] = 0
	
	puzzle = newGrid(size)
	for _ in range(1000):
		swapEmpty(puzzle)
	return puzzle

def newGrid(size):
	size_size = size * size
	puzzle = [-1 for _ in range(size_size)]
	cur = 1
	x = 0
	ix = 1
	y = 0
	iy = 0
	while True:
		puzzle[x + y * size] = cur
		if cur == 0:
			break
		cur += 1
		if x + ix == size or x + ix < 0 or (ix != 0 and puzzle[x + ix + y * size] != -1):
			iy = ix
			ix = 0
		elif y + iy == size or y + iy < 0 or (iy != 0 and puzzle[x + (y + iy) * size] != -1):
			ix = -iy
			iy = 0
		x += ix
		y += iy
		if cur == size_size:
			cur = 0
	return puzzle
