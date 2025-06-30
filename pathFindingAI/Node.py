# Autor - Guilherme Miranda 

class Node():

    def __init__(self, state, parent=None, action=None, cost=0, g=0):
        self.state =  state # MAPPROBLEM
        self.parent = parent
        self.action = action
        self.cost = cost
        self.g = g
        
        


