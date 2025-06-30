# Autor - Guilherme Miranda 

import MapProblem as mp
import Node as nd
import libskmapsV2 as mapsV2


def aStar(initialState):
    initialNode = nd.Node(initialState)

    visited = []
    queue = [initialNode]

    while True:
        if not queue:
            return None
        
        queue.sort(key=lambda x: x.state.heuristic() + x.g)  
        currentNode = queue.pop(0)

        if currentNode.state.isFinal():
            print("Found the goal!")
            return currentNode
        
        visited.append(currentNode)
        
        successors = currentNode.state.succ()
        for successor in successors:
            equalMaps = False
            newState = successor[0]
         
            # New map is not in visited or queue
            for node in visited + queue:
                if node.state.isEqual(newState):
                    equalMaps = True
                    break

            if not equalMaps:
                newNode = nd.Node(newState, currentNode, successor[1], successor[2], currentNode.g + 1)
                queue.append(newNode)
        

if __name__ == "__main__":
    
    map = mapsV2.readSkMap('./Mapas/rooms4.txt')
    
    print('====================')
    print('1 - Normal')
    print('2 - Diagonal')    
    print('====================')
    while True:
        try:
            typeProblem = int(input('Game mode: '))
            
            match typeProblem:
                case 1: 
                    node = aStar(mp.Problem(map))
                case 2:
                    node = aStar(mp.ProblemDiagonal(map))
                case _:
                    raise ValueError
                
            break
                
        except ValueError:
            print('Must enter a number between 1 and 2', end='\n\n')    


    if node is not None:
        actions = []
        cost = 0
        while node.parent != None:
            print(f'Action: {node.action}, Cost: {node.cost}, g(n): {node.g}')
            actions.append(node.action)
            cost += node.cost
            node = node.parent


        actions.reverse()             
        map2 = mapsV2.markPathSkMap(map, actions)
        

        if map2 is None:
            print("Error in Path!")
        else:
            mapsV2.printSkMap(map2)
            mapsV2.drawSkMap(map2,mapsV2.createWindow(400))
            print(f'Cost: {cost}')
            input("Enter para continuar... ")

    else:
        print("No solution found")