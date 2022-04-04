import numpy as np
from heapq import heappush, heappop

# --- INISIALISASI ---
goalState = [[1, 2, 3, 4], 
             [5, 6, 7, 8], 
             [9, 10, 11, 12], 
             [13, 14, 15, 16]]
# ^Tujuan/susunan akhir matriks

producedState_count = 0
# ^Jumlah state/susunan anak yang dihasilkan state parentnnya

# --- FUNGSI FUNGSI ---
def searchElement(puzzle, val):
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if puzzle[i][j] == val:
                return i, j 
# ^Fungsi untuk mencari indeks elemen pada suatu matriks

def getKurangI(puzzle):
    sumKurangI = 0
    for tiles in range(1,17):
        currRow, currCol = searchElement(puzzle, tiles)
        currKurangI = 0
        for inspectedRow in range(len(puzzle)):
            for inspectedCol in range(len(puzzle[inspectedRow])):
                if puzzle[inspectedRow][inspectedCol] < tiles:
                    if currRow == inspectedRow:
                        if inspectedCol > currCol:
                            currKurangI += 1
                    elif currRow < inspectedRow:
                        currKurangI += 1 
        sumKurangI += currKurangI
        print("Kurang(",tiles,") = ", currKurangI)
    return sumKurangI
# ^Fungsi unutuk mendapatkan nilai KURANG(i) dan jumlah totalnya

def getX(puzzle):
    n = 16
    i_blank, j_blank = searchElement(puzzle, n)
    temp = i_blank + j_blank
    if temp % 2 == 0:
        return 0
    else:
        return 1
# ^Fungsi untuk mendapatkan nilai X dari matriks

def getPuzzle(textFile):
    with open(textFile, 'r') as test:
        testLine = test.readlines()
    testLine = [row.strip() for row in testLine]
    testLine = [row.split(' ') for row in testLine]
    testLine = [[int(x) for x in row] for row in testLine]
    return np.array(testLine)
# ^Fungsi untuk mendapatkan matriks dari text file 

def stateCost(puzzle):
    currCost = 0
    for inspectedRow in range(len(puzzle)):
        for inspectedCol in range(len(puzzle[inspectedRow])):
            if puzzle[inspectedRow][inspectedCol] != 16:
                if puzzle[inspectedRow][inspectedCol] != goalState[inspectedRow][inspectedCol]:
                    currCost += 1
    return currCost
# ^Fungsi untuk menentukan cost dari setiap kemungkinan pergerakan blank cell

def isCrackable(puzzle):
    sumKurangI = getKurangI(puzzle) 
    xValue = getX(puzzle) 
    final = sumKurangI + xValue 
    print("\nNilai X = ", xValue) 
    print("\nJumlah(KURANG(i)) + X = ", final)
    if (final) % 2 == 0: # kalau genap
        print("Puzzle ini dapat diselesaikan :)")
        return True
    else: # kalau ganjil
        print("Maaf :( Puzzle ini tidak dapat diselesaikan")
        return False
# ^Fungsi untuk mencari tahu apakah puzzle dapat mencapai tujuan akhir

class priorityQueue:
    def __init__(own):
        own.heap = []

    def push(own, value):
        heappush(own.heap, value)

    def pop(own):
        return heappop(own.heap)

    def isEmpty(own):
        if not own.heap:
            return True
        else:
            return False
# ^Pembuatan kelas priority queue untuk menyimpan state/susunan dan costnya

class State:
    def __init__(own, root, puzzle, blankRow, blankCol, stateCost, depthLevel, prevMove): 
        own.root = root
        own.puzzle = puzzle
        own.stateCost = stateCost 
        own.depthLevel = depthLevel
        own.blankRow = blankRow 
        own.blankCol = blankCol 
        own.prevMove = prevMove

    def __lt__(own, other): 
        return own.stateCost < other.stateCost
# ^Pembuatan kelas node 

def getValidMove(blankRow, blankCol, prevMove): 
    validMove = ["Up", "Down", "Left", "Right"] 
    if blankRow == 3 or prevMove == "Up":
        validMove.remove("Down")
    if blankCol == 0 or prevMove == "Right":
        validMove.remove("Left")
    if blankRow == 0 or prevMove == "Down":
        validMove.remove("Up")
    if blankCol == 3 or prevMove == "Left": 
        validMove.remove("Right")
    return validMove
# ^Fungsi untuk mendapatkan daftar valid move dari suatu blank cell

def createChildState(state): 
    childState =[]
    validMove = []
    validMove = getValidMove(state.blankRow,state.blankCol ,state.prevMove)
    for move in validMove: 
        if move == "Right":
            newRow = state.blankRow
            newCol = state.blankCol + 1
        elif move == "Down": 
            newRow = state.blankRow + 1
            newCol = state.blankCol
        elif move == "Left": 
            newRow = state.blankRow
            newCol = state.blankCol - 1
        elif  move == "Up":
            newRow = state.blankRow - 1
            newCol = state.blankCol

        global producedState_count
        puzzle = state.puzzle 
        blankRow = state.blankRow
        blankCol = state.blankCol
        depthLevel = state.depthLevel
        
        newPuzzle = np.copy(puzzle) 
        save = newPuzzle[blankRow][blankCol]
        newPuzzle[blankRow][blankCol] = newPuzzle[newRow][newCol]
        newPuzzle[newRow][newCol] = save

        childState.append(State(state, newPuzzle, newRow, newCol, stateCost(newPuzzle) + depthLevel + 1, depthLevel+1, move))
        producedState_count += 1
    return childState
# ^Fungsi untuk membuat node/state child dari suatu node/state parent

def printStates(state): 
    if state.root == None:
        print("")
    else:
        printStates(state.root) 
        print("Berpindah : ", state.prevMove) 
        printPuzzle(state.puzzle)
# ^Fungsi untuk mencetak langkah-langkah yang dilakukan untuk mencapai tujuan akhir

def printPuzzle(puzzle):
    for inspectedRow in range(len(puzzle)):
        for inspectedCol in range(len(puzzle[inspectedRow])):
            if puzzle[inspectedRow][inspectedCol] == 16:
                print("-", end="\t")
            else: 
                print(puzzle[inspectedRow][inspectedCol], end="\t")
        print("")
    print("\n")
# ^Fungsi untuk mencetak puzzle

def solvePuzzle(puzzle):
    prioQ = priorityQueue()
    prioQ.push(State(None, puzzle, searchElement(puzzle, 16)[0], searchElement(puzzle,16)[1], stateCost(puzzle), 0, "None"))
    while not prioQ.isEmpty():
        node = prioQ.pop()
        if node.stateCost == 0 or node.stateCost == node.depthLevel: 
            
            printStates(node) 
            print("State anak yang dihasilkan = ", producedState_count) 
            return
        else:
            childState = createChildState(node)
            for child in childState: 
                prioQ.push(child)
# ^Fungsi untuk mencari solusi dari puzzle