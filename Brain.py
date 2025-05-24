import random
class Brain_Random():

    #returns x and y velocities
    def think(self):
        # initialize vels: cant either move vertically or horizontally at once
        possible = [1, -1]  # vels can be one or neg 1
        if random.random() > 0.5:
            return possible[random.randint(0, 1)] , 0
        else:
            return 0,  possible[random.randint(0, 1)]



class Brain_Manual():
    def __init__(self):
        self.next_move = (0,1 )

    #only set if direction is orthog
    def set_direction(self, direction):
        if self.next_move[0]*direction[0] +self.next_move[1]*direction[1] == 0 :
            self.next_move = direction

    def think(self ):
        return self.next_move


class Brain_NEAT():
    def __init__(self):
        pass