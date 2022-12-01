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
            print("Error: " + str(startLocation[0]) + str(startLocation[1]) + " is not a valid piece location")
            return False
        elif startLocation in self.boardDict:
            if self.boardDict[startLocation].blackwhite != turn:
                print("Error: It is " + turn + "'s turn to play")
                return False

            selectedPiece = self.boardDict[startLocation]
            validMoves = selectedPiece.findValidMoves(self.boardDict)

            self.boardDict[endLocation] = selectedPiece
            self.boardDict[endLocation].position = endLocation
            self.boardDict.pop(startLocation)

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
        numLoc = [0,0]
        numLoc[0] = ord(location[0]) - 65
        numLoc[1] = location[1] - 1

        return tuple(numLoc)

    def getBoardDict(self):
        return self.boardDict