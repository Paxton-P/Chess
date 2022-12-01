from .graphics import *
import numpy as np
import cv2

class Board:
    

    def __init__(self, height, width):
        self.h = height
        self.w = width
        self.win = GraphWin("Chess",750,750)
        self.lightSquares = "#faf6eb"
        self.darkSquares = "green"
        self.moveIndicatorCol = "lightgrey"

    def nextMove(self, boardDict, turn):
        origBoardDict = boardDict
        ptsMatrix = [[(0,0) for j in range(9)] for i in range(9)]

        for r in range(8):
            for c in range(8):
                pt = (c * self.w/8, r * self.h/8)

                ptsMatrix[r][c] = pt

                rect = Rectangle(Point(pt[0], pt[1]), Point(pt[0] + self.w/8,pt[1] + self.h/8))

                if (r + c) % 2 == 0:
                    rect.setFill(self.lightSquares)
                    rect.setOutline(self.lightSquares)
                    rect.draw(self.win)
                else:
                    rect.setFill(self.darkSquares)
                    rect.setOutline(self.darkSquares)
                    rect.draw(self.win)

        for pieceLoc in boardDict:
            piece = boardDict[pieceLoc]
            if piece.alive:
                print(piece)
                pieceImage = Image(Point((piece.position[0]) * self.h/8 + self.h/8/2, (7 - piece.position[1]) * self.w/8 + self.w/8/2), piece.img)
                pieceImage.draw(self.win)

        pieceLocation = (0,0)

        foundValidPiece = False
        while not foundValidPiece:

            #Pixel location from click
            pieceToMove = self.win.getMouse()

            #Piece Location with positive y coordinate downwards. Used for drawing purposes
            pieceLocationVis = (int(pieceToMove.getX() / (self.w/8)), int((pieceToMove.getY() / (self.h/8))))
            #Piece location in position coordinates where positive y is upwards
            pieceLocation = (pieceLocationVis[0], 7 - pieceLocationVis[1])

            #If square clicked contains a piece that is on the board, continue else continue trying to click on a piece
            if pieceLocation in boardDict:
                if boardDict[pieceLocation].blackwhite == turn:
                    foundValidPiece = True

        

        #Draw Circles for debugging and visualization purposes
        # pieceLocCircle = Circle(Point(pieceLocationVis[0] * self.w/8, pieceLocationVis[1] * self.h/8), 10)
        # selectCircle = Circle(pieceToMove, 10)
        # selectCircle.draw(self.win)
        # pieceLocCircle.draw(self.win)


        foundValidMove = False
        selectedPiece = boardDict[pieceLocation]
        # selectedPiece.printPiece()
        while not foundValidMove:
            #Find set of all valid moves that the selected piece can make
            validMoves = selectedPiece.findValidMoves(boardDict)
            
            for move in validMoves:
                moveIndicator = Circle(Point(move[0] * self.w/8 + self.w/8/2, (7 - move[1]) * self.h/8 + self.h/8/2), 13)
                moveIndicator.setFill(self.moveIndicatorCol)
                moveIndicator.setOutline(self.moveIndicatorCol)
                moveIndicator.draw(self.win)

            #Wait for click of valid move from user
            newLocation = self.win.getMouse()

            #Move Location with positive y coordinate downwards. Used for drawing purposes
            newLocationVis = (int(newLocation.getX() / (self.w/8)), int((newLocation.getY() / (self.h/8))))
            #Move location in position coordinates where positive y is upwards
            newLocationPos = (newLocationVis[0], 7 - newLocationVis[1])

            if newLocationPos == pieceLocation:
                #If the user selects the selected piece again then we look for new piece to be selected
                print("Reselect")
                return self.nextMove(origBoardDict, turn)
                
            elif newLocationPos in validMoves:
                print("Selected Valid Move")
                #If there was already a piece there capture it
                if newLocationPos in boardDict:
                    boardDict[newLocationPos].capture()

                #Delete the last location that the piece moved from
                del boardDict[pieceLocation]

                #Update piece position
                selectedPiece.position = newLocationPos
                boardDict[newLocationPos] = selectedPiece
                
                print("Updated board dict")
                print(newLocationPos)
                print(selectedPiece)
                return boardDict
            
                    



            pieceToMove = self.win.getMouse()
            notOver = False


    def evaluate(self, boardDict):
        eval = 0
        for key in boardDict:
            if boardDict[key].blackwhite == "white":
                eval = eval + boardDict[key].value
            else:
                eval = eval - boardDict[key].value
        return eval
