# Node Class to represent every number in the gameboard
class node:
    def __init__(self, number,x,y):
        # Number the node is set to
        self.number = number
        # The domain of possible values for this node, start as empty then fill up later
        self.domain = []
        # This node's coordinates in the board
        self.x = x
        self.y = y

    def modifyDomain(self,gameBoard):
        # Start the newDomain as a full domain
        newDomain = [1,2,3,4,5,6,7,8,9]
        # If the current node's number isn't 0, then it isn't empty. Remove it from the possible newDomain list
        if(self.number != 0):
            newDomain.remove(self.number)
        # Check for values that are in the same row as the current node
        for i in range(len(gameBoard[0])):
            if ((gameBoard[self.x][i].number != 0) and (self.y != i)):
                if(gameBoard[self.x][i].number in newDomain):
                    newDomain.remove(gameBoard[self.x][i].number)

        # Check for values that are in the same column as the current node
        for i in range(len(gameBoard)):
            if ((gameBoard[i][self.y].number != 0) and (self.x != i)):
                if(gameBoard[i][self.y].number in newDomain):
                    newDomain.remove(gameBoard[i][self.y].number)

        # Check for values that are in the same box as the current node
        box_x = self.y // 3
        box_y = self.x // 3
        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x * 3, box_x*3 + 3):
                if ((gameBoard[i][j].number != 0) and (i != self.x) and (j != self.y)):
                    if(gameBoard[i][j].number in newDomain):
                        newDomain.remove(gameBoard[i][j].number)
        # By now, constraints have restricted the domain, and we can set the current node's domain to newDomain
        self.domain = newDomain
        
"""
AC3()

The main AC3 function. It is a recursive function that tries to solve the board,
given the game constraints, but if it reaches a dead end it will continuously backtrack to try a different number for each spot.
What makes this different from regular backtracking is that the domain is reduced by constraints.

:param gameBoard: The 2D Array Board

:return: Returns a boolean, True if the board is solved, False if it couldn't be solved.
"""
def AC3(gameBoard):
    # Find empty space, set find to a node that represents an empty space or None if no empty space
    find = find_empty(gameBoard)
    #If no empty space, return True to end solved board.
    if not find:
        return True
    # Try each number in the empty space's domain
    for num in find.domain:
        # Set this node's space to num and modify the domain
        find.number = num
        fixDomain(gameBoard)
        # Attempt to solve the board from that pointer
        if (AC3(gameBoard)):
            return True
        # If the board wasn't solved yet, we will just set reset that space to an empty space and fix the domain
        find.number = 0
        fixDomain(gameBoard)
    
    return False
    

"""
backTrack()

The main Backtracking Search function. It is a recursive function that tries to solve the board,
given the game constraints, but if it reaches a dead end it will continuously backtrack to try a different number for each spot

:param gameBoard: The 2D Array Board

:return: Returns a boolean, True if the board is solved, False if it couldn't be solved.
"""
def backTrack(gameBoard):
    # Find empty space, set find to a node object located at that spot, or None if no empty space
    find = find_empty(gameBoard)
    #If no empty space, return True to end solved board. Otherwise set variables row and col equal to the coords of that empty space
    if not find:
        return True 
    else:
        row = find.x
        col = find.y
    
    # Attempt to place digits 1-9 in that space
    for i in range(1,10):
        # Check if that digit is valid in the current spot based on the board
        # If the digit is valid, recursively attempt to fill the board calling this solve() function again
        # If it isn't valid, reset the square that was just filled and go back to the previous step
        if (valid(gameBoard, i, row, col)):
            # Set this space to i
            gameBoard[row][col].number = i
            # Attempt to solve the board from that point
            if (backTrack(gameBoard)):
                return True
            # If the board wasn't solved yet, we will just set reset that space to an empty space
            gameBoard[row][col].number = 0
    
    return False

"""
valid()

Checks if a spot is valid or not.
There can only be one type of the number in each row, column, and box.

:param gameBoard: The 2D Array Board
:param num: The number we want to add into the space
:param row: The row index of the empty spot
:param col: The column index coordinate of the empty spot

:return: A boolean to determine if the move is a valid move or not.
"""
def valid(gameBoard, num, row, col):
    # Check for values that are in the same row as the current node
    for i in range(len(gameBoard[0])):
        if ((gameBoard[row][i].number == num) and (col != i)):
            return False

    # Check for values that are in the same column as the current node
    for i in range(len(gameBoard)):
        if ((gameBoard[i][col].number == num) and (row != i)):
            return False

    # Check for values that are in the same box as the current node
    box_x = col // 3
    box_y = row // 3
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if ((gameBoard[i][j].number == num) and (i != row) and (j != col)):
                return False

    return True


"""
find_empty()

Searches the game board for the next empty spot. Once found, returns the node object at that spot
If board isn't empty, return a null value.

:param gameBoard: The 2D Array Board

:return: A node object at that spot
"""
def find_empty(gameBoard):
    for i in range(len(gameBoard)):
        for j in range(len(gameBoard[0])):
            if (gameBoard[i][j].number == 0):
                return gameBoard[i][j]
    return None


"""
createBoard()

Populates a 2D array with node objects to represent the board

:param preGameBoard: a 2D array of ints representing the board

:return: A 2D array representation of the board with node objects
"""
def createBoard(preGameBoard):
    gameBoard = []
    tempRow = []
    for x in range(len(preGameBoard)):
        for y in range(len(preGameBoard[0])):
            tempRow.append(node(preGameBoard[x][y],x,y))
        # Add the nodes row by row
        gameBoard.append(tempRow.copy())
        tempRow.clear()
    return gameBoard

"""
convertString()

This function should take in a user's input string of 81 characters representing an unsolved Sudoku board.
Unassigned cells are marked with a "."

:param gridString: The user's input string of the board

:return: A 2D array representation of the board
"""
def convertString(gridString):
    gameBoard = []
    tempRow = []
    for i in range (82):
        if((i % 9 == 0) and (i != 0)):
            gameBoard.append(tempRow.copy()) #add the newly made row to the board
            tempRow.clear() #clear the temp row to start adding to the next row
        if(i < 81):
            if(gridString[i] == '.'):
                tempRow.append(0)
            else:
                tempRow.append(int(gridString[i]))
    return gameBoard

"""
printBoard()

Outputs the current state of the Sudoku board in the desired form

:param gameBoard: The 2D array representing the game board
"""
def printBoard(gameBoard):
    #Loop through the board and add a '|' in between every 3 numbers, and a row of 11 '-' after every third column
    for i in range(len(gameBoard)): #go through each row
        if((i % 3 == 0) and (i != 0)):
            print('-----------')
        for j in range(len(gameBoard[0])): #go through each column
            if((j % 3 == 0) and (j != 0)):
                print('|', end="")
            if(gameBoard[i][j].number == 0):
                print(".",end="")
            else:
                print(str(gameBoard[i][j].number),end="")
        print("")


"""
fixDomain()

Goes through every object in the game board and updates its domain to reflect the state of the board

:param gameBoard: The 2D array representing the game board
"""
def fixDomain(gameBoard):
    for x in range(9):
        for y in range(9):
            gameBoard[x][y].modifyDomain(gameBoard)

if __name__ == '__main__':
    # Create a board of integers from a string.
    # FOR TESTING - preGameBoard = convertString("..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..")
    # FOR TESTING - preGameBoard = convertString("...26.7.168..7..9.19...45..82.1...4...46.29...5...3.28..93...74.4..5..367.3.18...")

    preGameBoard = convertString(input("Please enter the unsolved Sudoku Grid string: "))
    # Using the board of ints, create a board full of objects
    gameBoard = createBoard(preGameBoard)
    # Make the initial domains
    fixDomain(gameBoard)

    print("\nCurrent Board:\n")
    printBoard(gameBoard)

    # Try AC3
    if(AC3(gameBoard)):
        print("\nFinished Board w/ AC3:\n")
        printBoard(gameBoard)
    else:
        print("The given board cannot be solved with AC3.")

    # Try Back Tracking
    if(backTrack(gameBoard)):
        print("\nFinished Board w/ Backtracking:\n")
        printBoard(gameBoard)
    else:
        print("The given board cannot be solved with Backtracking.")
    print("")
