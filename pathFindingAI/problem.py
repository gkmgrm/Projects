import libskmaps as maps
import heuristic as h


class Problem:
    """
    methods:
    init -> (map vem do ficheiro)
    isFinal() -> return bool
    heuristic() -> return value (number) herança (manhattan distance)
    succ() -> return list of tuples (node, action, cost)
    """
    def __init__ (self, map, heuristic : h.Heuristic):
        self.map = maps.readSkMap(map)
        self.playerPos = maps.foundPlayerSkMap(self.map)
        self.goalPos = self.findGoalSkMap()
        self.heuristicClass = heuristic
        self.moves = [("up", -1, 0), ("down", 1, 0), ("left", 0, -1), ("right", 0, 1)]

    def isFinal(self):
        return self.playerPos == self.goalPos

    def heuristic(self):
        return self.heuristicClass.distance(self.playerPos, self.goalPos)
    
    def succ(self):
        successors = []

        for move in self.moves:
            newPos = [self.playerPos[0] + move[1], self.playerPos[1] + move[2]]
            if self.map[newPos[0]][newPos[1]] != "#": # not a wall
                successors.append((newPos, move[0], 1))

        return successors


    def findGoalSkMap(self):
        for l in range(len(self.map)):
            for c in range(len(self.map[l])):
                if self.map[l][c] == ".":
                    return [l,c]
        return [-1,-1]
    




if __name__ == "__main__":
    
    #test = Problem('./Mapas/teste.txt', h.HeuristicManhattan)
    test = Problem('./Mapas/Minicosmos22c.txt', h.HeuristicManhattan)
    
    maps.printSkMap(test.map)
    print(f'{"Player pos":<17}-> {test.playerPos}')
    print(f'{"Goal pos":<17}-> {test.goalPos}')
    print(f'{"isFinal method":<17}-> {test.isFinal()}')
    print(f'{"heuristic method":<17}-> {test.heuristic()}')
    


    print(test.succ())