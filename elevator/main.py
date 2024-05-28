class Elevator(object):
    def __init__(self, cur_floor, direction):
        """
        Initializing function for Elevator class
        """
        self.floor = cur_floor
        self.direct = direction
    
    def move(self):
        """
        Moves an elevator by one step based on the direction
        """
        if self.direct == 'down':
            self.floor -= 1
        if self.direct == 'up':
            self.floor +=1