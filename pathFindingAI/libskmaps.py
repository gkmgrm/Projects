import math
import random
import copy
from tkinter import *
import MapProblem as problem


# --------------------------------------------------------
#
#   map: list of list of chars ("#", "@", ".", " ", "x", "+")
#   path: list of strings representing the 4 movements ("up", "down", "left", "right")
#                                             
#   readSkMap(file) -> map
#   printSkMap(map)
#   markPathSkMap(map, path) -> newMap or None
#
#   createWindow(size) -> windowsDefs
#   drawSkMap(map,windowsDefs) -> windowsDefs
#
"""
Funções para ler níveis (tabuleiros) de Sokoban.
Formato usual para os  níveis
   # Parede
   @ Jogador
   + Jogador numa posição objectivo
   $ Caixa
   * Caixa numa posição objectivo
   . Posição objectivo (local onde deve ser colocada uma caixa)
     Espaço em branco para as resptantes posições

Para mais informação consultar
   http://sokobano.de/wiki/index.php?title=Level_format 

ATENÇÃO: A leitura do mapas dos ficheiros só consideram:
   # Parede
   @ Jogador
   . A posição objectivo (a primeira que é encontada quando lê o mapa é lido)
Os restantes simbolos são ignorados e considerados como espaço em branco (vazio)

No entanto os seguintes simbolos são ainda utilizados.
   x indica que a posição já foi visitada pelo jogador
   + indica que o jogador está na posição final

Em vez do + a verificação do caminho utiliza as strings dos movimentos!!!


"""

# ---------------------------------------
#   Funções para ler de mapas (sokoban)
# ---------------------------------------

def addExtraEndSpaces(l, maxCol):
    for i in range(len(l), maxCol):
        l.append(" ")


def readRawSkMap(file):
    listaLinhas = []
    fin = open(file,"r")
    llinhas = fin.read().splitlines()

    maxCol = 0
    # Collect only non empty lines
    for l in llinhas:
        if l != "":
            listaLinhas.append(list(l))
            if len(l) > maxCol:
                maxCol = len(l)

    # add extra end spaces
    for l in listaLinhas:
        addExtraEndSpaces(l, maxCol)

    fin.close();
    return listaLinhas

def filterRawMap(rawMap):
    goalFound = False
    for l in range(len(rawMap)):
        for c in range(len(rawMap[l])):
            if rawMap[l][c] == "#":   # wall
                continue
            elif rawMap[l][c] == " ":   # empty space
                continue
            elif rawMap[l][c] == "@":   # player
                continue
            elif rawMap[l][c] == "." and not goalFound : # goal position
                goalFound = True
                continue
            else:           # everything else is assumed to be an empty space
                rawMap[l][c] = " "
    return rawMap

def readSkMap(file):
    return filterRawMap(readRawSkMap(file))

def printSkMap(map):
    for line in map:
        for col in line:
            if col == " ":
                print(" ", sep="", end="")
            elif col =="up":
                print("^", sep="", end="")
            elif col =="down":
                print("v", sep="", end="")
            elif col =="left":
                print("<", sep="", end="")
            elif col =="right":
                print(">", sep="", end="")
            else:
                print(col, sep="", end="")                
        print()


# ---------------------------------------------------
#   Função para verificar se um caminho é solução
# ---------------------------------------------------

def foundPlayerSkMap(map):
    for l in range(len(map)):
        for c in range(len(map[l])):
            if map[l][c] == "@":
                return [l,c]
    return [-1,-1]


def normalizeSkPath(path):
    return [m.lower() for m in path]

def makeMoveSkMap(map,pPos,dl,dc,m):

    if map[pPos[0]][pPos[1]] == "+":  # Trying to move from a goal state - IMPOSSIBLE
        return False
    
    l = pPos[0] + dl
    c = pPos[1] + dc

    if map[l][c] == "#":  # move to a Wall - ERROR!...
        return False

    if map[l][c] == ".":  # move to a goal cell
        map[l][c] = "+"
    else:                 # move to other cell
        map[l][c] = m     # mark that cell as visited
    pPos[0] = l
    pPos[1] = c
    return True

def applyMoveSkMap(map,pPos,m):
    if m == "up":
        return makeMoveSkMap(map,pPos ,-1,0,m)
    elif m == "down":
        return makeMoveSkMap(map,pPos ,+1,0,m)
    elif m == "left":
        return makeMoveSkMap(map,pPos ,0,-1,m)
    elif m == "right":
        return makeMoveSkMap(map,pPos ,0,+1,m)
    else:
        print(f"UNKNOWN move: {m}")
    
    return False

def applyPathSkMap(map,pPos,path):
    for m in path:
        if not applyMoveSkMap(map,pPos,m):
            return False
    
    # after applying moves check if player is in goal cell
    if map[pPos[0]][pPos[1]] == "+":
        return True
    else:
        return False

def markPathSkMap(map, path):
    mapaux = copy.deepcopy(map)
    pPos = foundPlayerSkMap(mapaux)

    if applyPathSkMap(mapaux,pPos,normalizeSkPath(path)):
        return mapaux
    else:
        return None

# --------------------------
#   Funcoes parte grafica
# --------------------------
def minmaxSkMap(map):
    lines = len(map)
    cols = len(map[0])

    if lines < cols:
        return lines,cols
    else:
        return cols,lines


def createWindow(tamanho):
    window = Tk()
    window.title("Map")
    window.geometry("+10+10")
    window.minsize(tamanho,tamanho)

    c = Canvas(window,bg="white", height=tamanho, width=tamanho)
    return window, c, tamanho

def drawSkArrow(canvas, xi, yi, xf, yf, dx, dy, boxSize):
    arrowSize = 5
    color = "black"
    w = 2
    x2 = (xi + xf) / 2
    y2 = (yi + yf) / 2
    
    canvas.create_line(x2,y2,
                       x2 - dx*(boxSize/2),
                       y2 - dy*(boxSize/2),
                       fill=color, width=w)
    
    canvas.create_line(x2,y2,
                       x2-(dx*boxSize/arrowSize)+(dy*boxSize/arrowSize),
                       y2-(dy*boxSize/arrowSize)+(dx*boxSize/arrowSize), 
                       fill=color, width=w)
    canvas.create_line(x2,y2,
                       x2-(dx*boxSize/arrowSize)-(dy*boxSize/arrowSize),
                       y2-(dy*boxSize/arrowSize)-(dx*boxSize/arrowSize), 
                       fill=color, width=w)

def drawSkBox(canvas,map,l,offsetL,c,offsetC,boxSize):
    espaco = boxSize*0.1
    xi = ((c + offsetC) * boxSize) + espaco
    yi = ((l + offsetL) * boxSize) + espaco
    xf = (xi + boxSize) - espaco
    yf = (yi + boxSize) - espaco

    if map[l][c] == "#":
        canvas.create_rectangle(xi,yi,xf,yf, fill="gray")
    elif map[l][c] == "@":
        canvas.create_rectangle(xi,yi,xf,yf, fill="blue")
    elif map[l][c] == ".":
        canvas.create_rectangle(xi,yi,xf,yf, fill="red")
    elif map[l][c] == "+":
        canvas.create_rectangle(xi,yi,xf,yf, fill="yellow")
    elif map[l][c] == "x":
        canvas.create_rectangle(xi,yi,xf,yf, fill="green")
    elif map[l][c] == "up":
        canvas.create_rectangle(xi,yi,xf,yf, fill="green")
        drawSkArrow(canvas,xi,yi,xf,yf,0,-1,boxSize)
    elif map[l][c] == "down":
        canvas.create_rectangle(xi,yi,xf,yf, fill="green")
        drawSkArrow(canvas,xi,yi,xf,yf,0,+1,boxSize)
    elif map[l][c] == "left":
        canvas.create_rectangle(xi,yi,xf,yf, fill="green")
        drawSkArrow(canvas,xi,yi,xf,yf,-1,0,boxSize)
    elif map[l][c] == "right":
        canvas.create_rectangle(xi,yi,xf,yf, fill="green")
        drawSkArrow(canvas,xi,yi,xf,yf,+1,0,boxSize)
    #else:
    #    canvas.create_rectangle(xi,yi,xf,yf, fill="white")


def drawSkMap(map, windefs):
    (window, canvas, wSize) = windefs
    canvas.delete('all')

    minCels, maxCels = minmaxSkMap(map)
    offsetCels = int((maxCels - minCels)/2)
    offsetL = 0
    offsetC = 0
    if len(map) == maxCels:  # lines > cols
        offsetC = offsetCels
    else:
        offsetL = offsetCels

    boxSize = wSize/maxCels

    for l in range(len(map)):
        for c in range(len(map[l])):
            drawSkBox(canvas,map,l,offsetL,c,offsetC,boxSize)

    canvas.pack()
    window.update()
    return windefs



# -------------------------
#   Para testar o código:
# -------------------------
if __name__ == "__main__":                              

    w = createWindow(400)

    map = readSkMap("./Mapas/Minicosmos22c.txt")

    mp = problem.Problem(map)
    print(f'heuristc -> {mp.heuristic()}')
    print(f'successors -> {mp.succ()}')

    printSkMap(map)
    drawSkMap(map,w)

    print("Map PATH:")
    map2 = markPathSkMap(map, ["up", "right", "right", "up", "up", "up", "left", "left"])
    if map2 is None:
        print("Error in Path!")
    else:
        printSkMap(map2)
        drawSkMap(map2,w)
        input("Enter para continuar... ")



