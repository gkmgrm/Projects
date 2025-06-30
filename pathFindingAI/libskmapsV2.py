import math
import random
import copy
from tkinter import *


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
FunÃ§Ãµes para ler nÃ­veis (tabuleiros) de Sokoban.
Formato usual para os  nÃ­veis
   # Parede
   @ Jogador
   + Jogador numa posiÃ§Ã£o objectivo
   $ Caixa
   * Caixa numa posiÃ§Ã£o objectivo
   . PosiÃ§Ã£o objectivo (local onde deve ser colocada uma caixa)
     EspaÃ§o em branco para as resptantes posiÃ§Ãµes

Para mais informaÃ§Ã£o consultar
   http://sokobano.de/wiki/index.php?title=Level_format 

ATENÃ‡ÃƒO: A leitura do mapas dos ficheiros sÃ³ consideram:
   # Parede
   @ Jogador
   . A posiÃ§Ã£o objectivo (a primeira que Ã© encontada quando o mapa Ã© lido)
Os restantes simbolos sÃ£o ignorados e considerados como espaÃ§o em branco (vazio)

No entanto os seguintes simbolos sÃ£o ainda utilizados.
   x indica que a posiÃ§Ã£o jÃ¡ foi visitada pelo jogador
   + indica que o jogador estÃ¡ na posiÃ§Ã£o final

Em vez do + a verificaÃ§Ã£o do caminho utiliza as strings dos movimentos!!!


"""

# ---------------------------------------
#   FunÃ§Ãµes para ler de mapas (sokoban)
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

    fin.close()
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
#   FunÃ§Ã£o para verificar se um caminho Ã© soluÃ§Ã£o
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
    if map[l][pPos[1]] == "#":  # diagonal vertical with a Wall - ERROR!...
        return False
    if map[pPos[0]][c] == "#":  # diagonal horizontal with a Wall - ERROR!...
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
    elif m == "up-left":
        return makeMoveSkMap(map,pPos ,-1,-1,m)
    elif m == "up-right":
        return makeMoveSkMap(map,pPos ,-1,+1,m)
    elif m == "down-left":
        return makeMoveSkMap(map,pPos ,+1,-1,m)
    elif m == "down-right":
        return makeMoveSkMap(map,pPos ,+1,+1,m)
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
    arrowSize = boxSize/4
    arrowAngle = math.pi/5
    color = "black"
    w = 2
    x2 = (xi + xf) / 2
    y2 = (yi + yf) / 2
    
    canvas.create_line(x2,y2,
                       x2 - dx*(boxSize/2),
                       y2 - dy*(boxSize/2),
                       fill=color, width=w)
   
    ang = math.atan2(dy,dx)

    ang += arrowAngle
    canvas.create_line(x2,y2,
                    x2-arrowSize*math.cos(ang),
                    y2-arrowSize*math.sin(ang), 
                    fill=color, width=w)

    ang -= 2*arrowAngle
    canvas.create_line(x2,y2,
                    x2-arrowSize*math.cos(ang),
                    y2-arrowSize*math.sin(ang), 
                    fill=color, width=w)


def drawSkBox(canvas,map,l,offsetL,c,offsetC,boxSize):
    espaco = boxSize*0.1
    xi = ((c + offsetC) * boxSize) + espaco
    yi = ((l + offsetL) * boxSize) + espaco
    xf = (xi + boxSize) - espaco
    yf = (yi + boxSize) - espaco

    if map[l][c] == "#":
        canvas.create_rectangle(xi,yi,xf,yf, fill="gray", outline="gray")
    elif map[l][c] == "@":
        canvas.create_rectangle(xi,yi,xf,yf, fill="blue", outline="blue")
    elif map[l][c] == ".":
        canvas.create_rectangle(xi,yi,xf,yf, fill="red", outline="red")
    elif map[l][c] == "+":
        canvas.create_rectangle(xi,yi,xf,yf, fill="yellow", outline="yellow")
    elif map[l][c] == "x":
        canvas.create_rectangle(xi,yi,xf,yf, fill="green", outline="green")
    elif map[l][c] == "up":
        canvas.create_rectangle(xi,yi,xf,yf, fill="green", outline="green")
        drawSkArrow(canvas,xi,yi,xf,yf,0,-1,boxSize)
    elif map[l][c] == "down":
        canvas.create_rectangle(xi,yi,xf,yf, fill="green", outline="green")
        drawSkArrow(canvas,xi,yi,xf,yf,0,+1,boxSize)
    elif map[l][c] == "left":
        canvas.create_rectangle(xi,yi,xf,yf, fill="green", outline="green")
        drawSkArrow(canvas,xi,yi,xf,yf,-1,0,boxSize)
    elif map[l][c] == "right":
        canvas.create_rectangle(xi,yi,xf,yf, fill="green", outline="green")
        drawSkArrow(canvas,xi,yi,xf,yf,+1,0,boxSize)
    
    elif map[l][c] == "up-left":
        canvas.create_rectangle(xi,yi,xf,yf, fill="green", outline="green")
        drawSkArrow(canvas,xi,yi,xf,yf,-1,-1,boxSize)
    elif map[l][c] == "up-right":
        canvas.create_rectangle(xi,yi,xf,yf, fill="green", outline="green")
        drawSkArrow(canvas,xi,yi,xf,yf,+1,-1,boxSize)
    elif map[l][c] == "down-left":
        canvas.create_rectangle(xi,yi,xf,yf, fill="green", outline="green")
        drawSkArrow(canvas,xi,yi,xf,yf,-1,+1,boxSize)
    elif map[l][c] == "down-right":
        canvas.create_rectangle(xi,yi,xf,yf, fill="green", outline="green")
        drawSkArrow(canvas,xi,yi,xf,yf,+1,+1,boxSize)

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
#   Para testar o cÃ³digo:
# -------------------------
if __name__ == "__main__":

    w = createWindow(400)

    map = readSkMap("./Mapas/Minicosmos22c.txt")
    #printSkMap(map)
    drawSkMap(map,w)
    input("Enter para continuar... ")

    print("Map PATH:")
    path = ["up", "right", "right", "up", "up", "up", "left", "left"]
    path = ["up-right", "right", "up", "up", "up-left", "left"]
    path = ['left', 'up', 'right', 'right', 'right', 'down', 'down-right',
            'right', 'right', 'up-right', 'up', 'up', 'up', 'up', 'left',
            'down-left', 'up-left', 'left', 'left', 'left'
            ]

    #print(path)
    map2 = markPathSkMap(map, path)
    if map2 is None:
        print("Error in Path!")
    else:
        #printSkMap(map2)
        drawSkMap(map2,w)
        input("Enter para continuar... ")


