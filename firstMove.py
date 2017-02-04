class Jobs:
    SCOUT = 0
    COLLECTOR = 1

class JobRegions:
    W = 0
    NW = 1
    N = 2
    NE = 3
    E = 4
    SE = 5
    S = 6
    SW = 7

nScouts = 8*2

def firstMove(self, view):

    # Check W (cuz west is best)
    if view[2][1][1] < nScouts/8:
        self.job = Jobs.SCOUT
        self.jobRegion = JobRegions.W
        return makeMove((Actions.MOVE_W, Actions.DROP_NONE))
    
    # Check NW
    elif view[1][1][1] < nScouts/8:
        self.job = Jobs.SCOUT
        self.jobRegion = JobRegions.NW
        return makeMove((Actions.MOVE_NW, Actions.DROP_NONE))
    
    # Check N
    elif view[1][2][1] < nScouts/8:
        self.job = Jobs.SCOUT
        self.jobRegion = JobRegions.N
        return makeMove((Actions.MOVE_N, Actions.DROP_NONE))
    
    # Check NE
    elif view[1][3][1] < nScouts/8:
        self.job = Jobs.SCOUT
        self.jobRegion = JobRegions.NE
        return makeMove((Actions.MOVE_NE, Actions.DROP_NONE))
        
    # Check E
    elif view[2][3][1] < nScouts/8:
        self.job = Jobs.SCOUT
        self.jobRegion = JobRegions.E
        return makeMove((Actions.MOVE_E, Actions.DROP_NONE))
        
    # Check SE
    elif view[3][3][1] < nScouts/8:
        self.job = Jobs.SCOUT
        self.jobRegion = JobRegions.SE
        return makeMove((Actions.MOVE_SE, Actions.DROP_NONE))
        
    # Check S
    elif view[3][2][1] < nScouts/8:
        self.job = Jobs.SCOUT
        self.jobRegion = JobRegions.S
        return makeMove((Actions.MOVE_S, Actions.DROP_NONE))
        
    # Check SW
    elif view[3][1][1] < nScouts/8:
        self.job = Jobs.SCOUT
        self.jobRegion = JobRegions.SW
        return makeMove((Actions.MOVE_SW, Actions.DROP_NONE))

    # Guess you're just a collector
    else:
        self.job = Jobs.COLLECTOR
        return makeMove((Actions.DROPOFF, Actions.DROP_NONE))
