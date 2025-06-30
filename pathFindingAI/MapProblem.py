# Autor - Guilherme Miranda

import libskmapsV2 as maps
import copy
from math import sqrt

class Problem:
    """
    methods:
    init -> (map vem do ficheiro)
    isFinal() -> return bool
    heuristic() -> return value (number) herança (manhattan distance)
    succ() -> return list of tuples (MapProblem, action, cost)
    isEqual(self, mapProblem) -> bool 
    """
    def __init__ (self, map):
        self.map = map
        self.playerPos = maps.foundPlayerSkMap(self.map)
        self.goalPos = self.findGoalSkMap(self.map)

    def isFinal(self):
        return self.playerPos == self.goalPos or self.map[self.playerPos[0]][self.playerPos[1]] == "+"

    def heuristic(self):
        return abs(self.playerPos[0] - self.goalPos[0]) + abs(self.playerPos[1] - self.goalPos[1])
    
    def succ(self):
        successors = []
        moves = [
            ("up", -1, 0, 1), ("down", 1, 0, 1), ("left", 0, -1, 1), ("right", 0, 1, 1)
        ]

        for move in moves:
            newRow = self.playerPos[0] + move[1]
            newCol = self.playerPos[1] + move[2]

            if (
                # not out of bounds, not a wall
                0 <= newRow < len(self.map) and 
                0 <= newCol < len(self.map[newRow]) and
                self.map[newRow][newCol] != "#"
            ):
                mapSucc = self.successorMap(move[0])
                successors.append((Problem(mapSucc), move[0], move[3]))

        
        return successors


    def isEqual(self, mapProblem):
        for l in range(len(self.map)):
            for c in range(len(self.map[l])):
                if self.map[l][c] != mapProblem.map[l][c]:
                    return False
        return True
    
    def successorMap(self, move):
        '''
        Return a new map
        '''
        newMap = copy.deepcopy(self.map)
        plyearPos = self.playerPos.copy()


        newMap[plyearPos[0]][plyearPos[1]] = ' '

        match move:
            case "up":
                plyearPos[0] -= 1
            case "down":
                plyearPos[0] += 1
            case "left":
                plyearPos[1] -= 1
            case "right":
                plyearPos[1] += 1


        if self.findGoalSkMap(newMap) == plyearPos:
            newMap[plyearPos[0]][plyearPos[1]] = "+"
            return newMap
        
        newMap[plyearPos[0]][plyearPos[1]] = "@"

        return newMap

    def findGoalSkMap(self, map):
        for l in range(len(map)):
            for c in range(len(map[l])):
                if map[l][c] == ".":
                    return [l,c]
        return [-1,-1]


class ProblemDiagonal(Problem):
    
    def succ(self):
        successors = []
        moves = [
            ("up", -1, 0, 1), ("down", 1, 0, 1), ("left", 0, -1, 1), ("right", 0, 1, 1),
            ("up-left", -1,-1, sqrt(2)), 
            ("up-right", -1,1, sqrt(2)),
            ("down-left", 1,-1, sqrt(2)),
            ("down-right", 1, 1, sqrt(2))
        ]

        for move in moves:
            newRow = self.playerPos[0] + move[1]
            newCol = self.playerPos[1] + move[2]
            
            if ( 
                # not out of bounds, not a wall, 
                # diagonal vertical with a Wall - ERROR!, diagonal horizontal with a Wall - ERROR!
                
                0 <= newRow < len(self.map) and 
                0 <= newCol < len(self.map[newRow]) and
                self.map[newRow][newCol] != "#" and  
                self.map[newRow][self.playerPos[1]] != '#' and 
                self.map[self.playerPos[0]][newCol] != '#' 
            ):
                mapSucc = self.successorMap(move[0])
                successors.append((ProblemDiagonal(mapSucc), move[0], move[3]))

        return successors
    
    def successorMap(self, move):
        '''
        Return a new map
        '''
        newMap = copy.deepcopy(self.map)
        plyearPos = self.playerPos.copy()


        newMap[plyearPos[0]][plyearPos[1]] = ' '

        match move:
            case "up":
                plyearPos[0] -= 1
            case "down":
                plyearPos[0] += 1
            case "left":
                plyearPos[1] -= 1
            case "right":
                plyearPos[1] += 1
            case 'up-left':
                plyearPos[0] -= 1
                plyearPos[1] -= 1
            case 'up-right':
                plyearPos[0] -= 1
                plyearPos[1] += 1
            case 'down-left':
                plyearPos[0] += 1
                plyearPos[1] -= 1
            case 'down-right':
                plyearPos[0] += 1
                plyearPos[1] += 1
        
        if self.findGoalSkMap(newMap) == plyearPos:
            newMap[plyearPos[0]][plyearPos[1]] = "+"
            return newMap
        
        newMap[plyearPos[0]][plyearPos[1]] = "@"

        return newMap
    
       


if __name__ == "__main__":
    
    pass