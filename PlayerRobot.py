from robot import Robot
from constants import Actions, TileType, SetupConstants
import random
import time
import math

zig_size = 2
num_scouts = 16

class Jobs:
    SCOUT = 0
    COLLECTOR = 1

class player_robot(Robot):
    def __init__(self, args):
        super(self.__class__, self).__init__(args)
        self.toHome = []
        self.numturns = SetupConstants.NUM_TURNS
        self.goinghome = False
        self.targetPath = None
        self.targetDest = (0,0)
        self.x = 0
        self.y = 0
        self.visited = []
        self.isFirstMove = True

    # A couple of helper functions (Implemented at the bottom)
    def undoAction(self, direction): return
    def ViewScan(self, view): return
    def FindRandomPath(self, view): return
    def UpdateTargetPath(self): return
    def firstMove(self, view): return
    def move_to_constant(self, view): return
    def next_move(self, view): return
    def round_away(self, view): return

    def get_move(self, view):
        if self.isFirstMove:
            self.isFirstMove = False
            return self.firstMove(view)

        if self.job == Jobs.SCOUT:
            return self.makeMove((self.next_move(view), Actions.DROP_NONE))

        else:
            return (Actions.DROPOFF, Actions.DROP_NONE)
            # Go home if you have no time or are full
            movesLeft = SetupConstants.NUM_TURNS - self.get_turn()
            if movesLeft <= len(self.toHome) or self.storage_remaining() == 0:
                if self.toHome == []: return (Actions.DROPOFF, Actions.DROP_NONE)
                undoAction = self.undoAction(self.toHome.pop())
                return (undoAction, Actions.DROP_NONE)

            # Search for resources; Updates self.targetPath, sefl.targetDest
            self.ViewScan(view)

            actionToTake = None
            if self.targetPath == None:
                actionToTake = self.FindRandomPath(view)

            elif(self.targetPath == []):
                self.targetPath = None
                return (Actions.MINE, Actions.DROP_NONE)
            else: actionToTake = self.UpdateTargetPath()

            self.toHome.append(actionToTake)
            markerDrop = random.choice([Actions.DROP_RED,Actions.DROP_YELLOW,Actions.DROP_GREEN,Actions.DROP_BLUE,Actions.DROP_ORANGE])
            #markerDrop = Actions.DROP_NONE
            return (actionToTake, markerDrop)


    # Returns opposite direction
    def undoAction(self, prevAction):
        if(prevAction == Actions.MOVE_N): return Actions.MOVE_S
        elif(prevAction == Actions.MOVE_NE): return Actions.MOVE_SW
        elif(prevAction == Actions.MOVE_E): return Actions.MOVE_W
        elif(prevAction == Actions.MOVE_SE): return Actions.MOVE_NW
        elif(prevAction == Actions.MOVE_S): return Actions.MOVE_N
        elif(prevAction == Actions.MOVE_SW): return Actions.MOVE_NE
        elif(prevAction == Actions.MOVE_W): return Actions.MOVE_E
        elif(prevAction == Actions.MOVE_NW): return Actions.MOVE_SE
        else: return Actions.MOVE_S


    # Scans the entire view for resource searching
    # REQUIRES: view (see call location)
    def ViewScan(self, view):
        viewLen = len(view)
        queue = [[(0,0)]]
        deltas = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]
        visited = set()
        visited.add((0,0))
        targetDepleted = (view[self.targetDest[0]][self.targetDest[1]][0].GetType() == TileType.Resource and
                         view[self.targetDest[0]][self.targetDest[1]][0].AmountRemaining() <= 0)
        # BFS TO find the next resource within your view
        if(self.targetPath == None or targetDepleted):
            while(len(queue)>0):
                path = queue[0]
                loc = path[0]
                queue = queue[1:]
                viewIndex = (loc[0] + viewLen//2,loc[1]+viewLen//2)
                if (view[viewIndex[0]][viewIndex[1]][0].GetType() == TileType.Resource and
                    view[viewIndex[0]][viewIndex[1]][0].AmountRemaining() > 0):
                    # print(path)
                    self.targetPath = path[1:]
                    self.targetDest = path[0]
                    return
                elif(view[viewIndex[0]][viewIndex[1]][0].CanMove()):
                    for i in range(8):
                        x = loc[0] + deltas[i][0]
                        y = loc[1] + deltas[i][1]
                        if(abs(x) <= viewLen//2 and abs(y) <= viewLen//2):
                            if((x,y) not in visited):
                                queue.append([(x,y)] + path[1:] + [deltas[i]])
                                visited.add((x,y))
        return


    # Picks a random move based on the view - don't crash into mountains!
    # REQUIRES: view (see call location)
    def FindRandomPath(self, view):
        viewLen = len(view)
        while(True):
            actionToTake = random.choice([Actions.MOVE_E,Actions.MOVE_N,
                                          Actions.MOVE_S,Actions.MOVE_W,
                                          Actions.MOVE_NW,Actions.MOVE_NE,
                                          Actions.MOVE_SW,Actions.MOVE_SE])
            if ((actionToTake == Actions.MOVE_N and view[viewLen//2-1][viewLen//2][0].CanMove()) or
               (actionToTake == Actions.MOVE_S and view[viewLen//2+1][viewLen//2][0].CanMove()) or
               (actionToTake == Actions.MOVE_E and view[viewLen//2][viewLen//2+1][0].CanMove()) or
               (actionToTake == Actions.MOVE_W and view[viewLen//2][viewLen//2-1][0].CanMove()) or
               (actionToTake == Actions.MOVE_NW and view[viewLen//2-1][viewLen//2-1][0].CanMove()) or
               (actionToTake == Actions.MOVE_NE and view[viewLen//2-1][viewLen//2+1][0].CanMove()) or
               (actionToTake == Actions.MOVE_SW and view[viewLen//2+1][viewLen//2-1][0].CanMove()) or
               (actionToTake == Actions.MOVE_SE and view[viewLen//2+1][viewLen//2+1][0].CanMove()) ):
               return actionToTake
        return None


    # Returns actionToTake
    # REQUIRES: self.targetPath != []
    def UpdateTargetPath(self):
        actionToTake = None
        (x, y) = self.targetPath[0]
        if(self.targetPath[0] == (1,0)):
            actionToTake = Actions.MOVE_S
        elif(self.targetPath[0] == (1,1)):
            actionToTake = Actions.MOVE_SE
        elif(self.targetPath[0] == (0,1)):
            actionToTake = Actions.MOVE_E
        elif(self.targetPath[0] == (-1,1)):
            actionToTake = Actions.MOVE_NE
        elif(self.targetPath[0] == (-1,0)):
            actionToTake = Actions.MOVE_N
        elif(self.targetPath[0] == (-1,-1)):
            actionToTake = Actions.MOVE_NW
        elif(self.targetPath[0] == (0,-1)):
            actionToTake = Actions.MOVE_W
        elif(self.targetPath[0] == (1,-1)):
            actionToTake = Actions.MOVE_SW
        # Update destination using path
        self.targetDest = (self.targetDest[0]-x, self.targetDest[1]-y)
        # We will continue along our path
        self.targetPath = self.targetPath[1:]
        return actionToTake


    def round_away(self, x):
        # round x away from 0
        if x == 0: return round(random.random()) * 2 - 1
        if x < 0: x = math.floor(x)
        else: x = math.ceil(x)
        if x > 1: return 1
        if x < -1: return -1
        return x


    def move_to_constant(self, x, y):
        return [
            [None,           Actions.MOVE_E,  Actions.MOVE_W],
            [Actions.MOVE_N, Actions.MOVE_NE, Actions.MOVE_NW],
            [Actions.MOVE_S, Actions.MOVE_SE, Actions.MOVE_SW]
        ][y][x]


    def next_move(self, view):
        x = self.x
        y = self.y
        # returns the next step, disregarding mountains
        angle = (self.direction / num_scouts) * 2 * math.pi
        optimal_x = math.cos(angle) * (self.get_turn() + 1)
        optimal_y = math.sin(angle) * (self.get_turn() + 1)
        move_x = optimal_x - x
        move_y = optimal_y - y
        move = (self.round_away(move_x), self.round_away(move_y))
        # diags = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        # normals = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        # while view[2 + move[0]][2 + move[1]][0] == TileType.Mountain and \
        #       (x + move[0], y + move[1]) not in self.history:
        #     if len(diags) > 0:
        #         i = math.floor(random.random() * len(diags))
        #         move = diags.pop(i)
        #     elif len(normals) > 0:
        #         i = math.floor(random.random() * len(normals))
        #         move = normals.pop(i)
        #     else:
        #         last = self.history[-1]
        #         return self.move_to_constant(last - x, last - y)
        return self.move_to_constant(*move)


    def firstMove(self, view):
        total = view[2][1][1] + view[1][1][1] + view[1][2][1] + view[1][3][1] + view[2][3][1] + view[3][3][1] + view[3][2][1] + view[3][1][1]
        self.direction = total
        if total <= num_scouts:
            self.job = Jobs.SCOUT
            move = self.next_move(view)
            return self.makeMove((move, Actions.DROP_NONE))
        else:
            moves = [ Actions.MOVE_N,
                      Actions.MOVE_E,
                      Actions.MOVE_S,
                      Actions.MOVE_W,
                      Actions.MOVE_NW,
                      Actions.MOVE_NE,
                      Actions.MOVE_SW,
                      Actions.MOVE_SE ]
            # return self.makeMove((random.choice(moves), Actions.DROP_NONE))
            self.job = Jobs.COLLECTOR
            return self.makeMove((Actions.DROPOFF, Actions.DROP_NONE))


    def makeMove(self, move):
        action, marker = move
        if action == Actions.MOVE_N:
            self.x -= 1
        elif action == Actions.MOVE_NE:
            self.x -= 1
            self.y += 1
        elif action == Actions.MOVE_E:
            self.y += 1
        elif action == Actions.MOVE_SE:
            self.y += 1
            self.x += 1
        elif action == Actions.MOVE_S:
            self.x += 1
        elif action == Actions.MOVE_SW:
            self.x += 1
            self.y -= 1
        elif action == Actions.MOVE_W:
            self.x -= 1
        elif action == Actions.MOVE_NW:
            self.x -= 1
            self.y -= 1
        self.toHome.append(action)
        return (action, marker)
