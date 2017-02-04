import random

from scout import next_move, num_scouts

class Jobs:
    SCOUT = 0
    COLLECTOR = 1

def firstMove(self, view):
    total = view[2][1][1] + view[1][1][1] + view[1][2][1] + view[1][3][1] + view[2][3][1] + view[3][3][1] + view[3][2][1] + view[3][1][1]
    self.direction = total
    if total <= num_scouts:
        self.job = Jobs.SCOUT
        move = next_move(view, [], (0, 0), self.direction, 1)
        return makeMove((move, Actions.DROP_NONE))
    else:
        moves = [ MOVE_N,
                  MOVE_E,
                  MOVE_S,
                  MOVE_W,
                  MOVE_NW,
                  MOVE_NE,
                  MOVE_SW,
                  MOVE_SE ]
        return makeMove((random.choice(moves), Actions.DROP_NONE))
        self.job = Jobs.COLLECTOR
