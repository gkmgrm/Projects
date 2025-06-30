from math import sqrt

class Heuristic:
    
    def distance(playerPos, goalPos):
        raise NotImplementedError("Subclasses should implement this!")


class HeuristicManhattan(Heuristic):

    def distance(playerPos, goalPos):
        return abs(playerPos[0] - goalPos[0]) + abs(playerPos[1] - goalPos[1])
