
def makeMove(self, (action, marker)):
    
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
    
    return (action, marker)
