from graphics.graphics import test
from .piece import Piece

class Knight(Piece):

    def __init__(self, position, blackwhite):
        super().__init__(position, blackwhite)
        self.img = 'none'
        if self.blackwhite == 'black':
            self.img = 'graphics/images/bkn_11.png'
        elif self.blackwhite == 'white':
            self.img = 'graphics/images/wkn_11.png'

    def printPiece(self):
        print(self.blackwhite + " Knight: " + str(self.position[0]) + " " + str(self.position[1]) + " Alive:" + str(self.alive))

    def __str__(self):
        return "Knight: " + self.blackwhite + " (" + str(self.position[0]) + "," + str(self.position[1]) + ")"

    def findValidMoves(self, boardDict):
        validMoves = set()

        for i in range(8):

            if i == 0:
                x = self.position[0] - 1
                y = self.position[1] + 2
            elif i == 1:
                x = self.position[0] + 1
                y = self.position[1] + 2
            elif i == 2:
                x = self.position[0] + 2
                y = self.position[1] + 1
            elif i == 3:
                x = self.position[0] + 2
                y = self.position[1] - 1
            elif i == 4:
                x = self.position[0] + 1
                y = self.position[1] - 2
            elif i == 5:
                x = self.position[0] - 1
                y = self.position[1] - 2
            elif i == 6:
                x = self.position[0] - 2
                y = self.position[1] - 1
            elif i == 7:
                x = self.position[0] - 2
                y = self.position[1] + 1

            testPos = (x,y)
            if Piece.validPos(testPos):
                if testPos in boardDict:
                    if boardDict[testPos].blackwhite != self.blackwhite:
                            validMoves.add(testPos)
                else:
                    validMoves.add(testPos)

        return validMoves