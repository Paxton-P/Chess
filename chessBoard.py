import numpy as np
import cv2

class ChessBoard:

    def __init__(self, boardDict):
        self.boardDict = boardDict

    def movePiece(self, startLocation, endLocation, turn):
        print(startLocation)
        print(endLocation)
        startLocation = self.stringLocationToNumLocation(startLocation)
        endLocation = self.stringLocationToNumLocation(endLocation)

        print(startLocation)
        print(endLocation)
        if startLocation not in self.boardDict:
            print("Error: " + startLocation + " is not a valid piece location")
            return
        elif startLocation in self.boardDict:
            if self.boardDict[startLocation].blackwhite != turn:
                print("Error: It is " + turn + "'s turn to play")


            selectedPiece = self.boardDict[startLocation]

            validMoves = selectedPiece.findValidMoves(self.boardDict)
            print(validMoves)


        return self.boardDict

    def evaluate(self):
        eval = 0
        for key in self.boardDict:
            if self.boardDict[key].blackwhite == "white":
                eval = eval + self.boardDict[key].value
            else:
                eval = eval - self.boardDict[key].value
        return eval

    def stringLocationToNumLocation(self, location):
        numLoc = (0,0)
        numLoc[0] = ord(location[0]) - 97
        numLoc[1] = ord(location[1]) - 48

        return numLoc

    def getBoardDict(self):
        return self.boardDict