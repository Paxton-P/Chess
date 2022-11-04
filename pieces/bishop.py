from .piece import Piece

class Bishop(Piece):

    def __init__(self, position, blackwhite):
        super().__init__(position, blackwhite)
        self.img = 'none'
        if self.blackwhite == 'black':
            self.img = 'graphics/images/bb_11.png'
        elif self.blackwhite == 'white':
            self.img = 'graphics/images/wb_11.png'

    def printPiece(self):
        print(self.blackwhite + " Bishop: " + str(self.position[0]) + " " + str(self.position[1]) + " Alive:" + str(self.alive))

    def __str__(self):
        return "Bishop: " + self.blackwhite + " (" + str(self.position[0]) + "," + str(self.position[1]) + ")"

    def findValidMoves(self, boardDict):
        validMoves = set()

        validMoves.update(self.findMovesWithDirection("up-left", boardDict))
        validMoves.update(self.findMovesWithDirection("up-right", boardDict))
        validMoves.update(self.findMovesWithDirection("down-left", boardDict))
        validMoves.update(self.findMovesWithDirection("down-right", boardDict))

        return validMoves

    def findMovesWithDirection(self, direction, boardDict):
        #Movement Up the board
        inc = (0,0)

        validMoves = set()

        if direction == "up-left":
            inc = (-1,1)
        elif direction == "up-right":
            inc = (1,1)
        elif direction == "down-left":
            inc = (-1,-1)
        elif direction == "down-right":
            inc = (1,-1)

        i = inc

        print(type(inc))

        testPos = self.position
        print(type(testPos))
        test = True
        while test:
            #Check to see if movement is in bounds of the board
            print(inc)
            testPos =   tuple([sum(x) for x in zip(testPos, inc)])
            print(type(testPos))
            if not Piece.validPos(testPos): 
                test = False
            else:
                #Check if piece is in the test posistion
                if testPos in boardDict:
                    #If their is already a piece on the board then check to see if it is an opposite colored piece
                    if boardDict[testPos].blackwhite != self.blackwhite:
                        #Add move that captures piece
                        validMoves.add(testPos)
                        #Done looking up
                        test = False
                    else:
                        #Done looking up
                        test = False
                else:
                    validMoves.add(testPos)

        return validMoves