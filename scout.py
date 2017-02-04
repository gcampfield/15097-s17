from __future__ import division, print_function
# functions to be used by the scout robot
import random
import math
from constants import TileType

zig_size = 2
num_scouts = 16

def round_away(x):
    # round x away from 0
    if x == 0: return round(random.random()) * 2 - 1

    if x < 0: x = math.floor(x)
    else: x = math.ceil(x)

    if x > 1: return 1
    if x < -1: return -1
    return x

def next_move(view, history, (x, y), direction, turn):
    # returns the next step, disregarding mountains
    angle = (direction / num_scouts) * 2 * math.pi

    optimal_x = math.cos(angle) * turn
    optimal_y = math.sin(angle) * turn

    move_x = optimal_x - x
    move_y = optimal_y - y

    move = (round_away(move_x), round_away(move_y))

    diags = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
    normals = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    while view[2 + move[0]][2 + move[1]][0] == TileType.Mountain and \
          (x + move[0], y + move[1]) not in history:
        if len(diags) > 0:
            i = math.floor(random.random() * len(diags))
            move = diags.pop(i)
        elif len(normals) > 0:
            i = math.floor(random.random() * len(normals))
            move = normals.pop(i)
        else:
            last = history[-1]
            return (last - x, last - y)
            
    return move

def test_next():
    # test next move function
    for d in range(num_scouts):
        # print("=" * 25 + " " + str(d) + " " + "=" * 25)
        curr = (0, 0)
        for i in range(1, 1000):
            move = next_move(curr, d, i)
            # print(move, end=" => ")
            assert(-1 <= move[0] <= 1)
            assert(-1 <= move[1] <= 1)
            curr = (curr[0] + move[0], curr[1] + move[1])
            # print(curr)
