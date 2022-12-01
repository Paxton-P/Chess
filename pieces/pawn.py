from .piece import Piece

class Pawn(Piece):

    value = 1

    def __init__(self, position, blackwhite):
        super().__init__(position, blackwhite)
        self.img = 'none'
        if self.blackwhite == 'black':
            self.img = 'graphics/images/bp_7_13.png'
        elif self.blackwhite == 'white':
            self.img = 'graphics/images/wp_13.png'
        
        self.firstMove = True

    def printPiece(self):
        print(self.blackwhite + " Pawn: " + str(self.position[0]) + " " + str(self.position[1]) + " Alive:" + str(self.alive))

    def __str__(self):
        return "Pawn: " + self.blackwhite + " (" + str(self.position[0]) + "," + str(self.position[1]) + ")"

    def findValidMoves(self, boardDict):
        validMoves = set()

        if self.blackwhite == "white":
            #Check if there is a piece in front of the pawn
            if (self.position[0], self.position[1] + 1) not in boardDict:
                validMoves.add((self.position[0], self.position[1] + 1))

                #Check to see if this is the first move the pawn has made. If so check to see if the pawn can move two spaces forward
                if self.position[1] == 1:
                    if (self.position[0], self.position[1] + 2) not in boardDict:
                        validMoves.add((self.position[0], self.position[1] + 2))
            

            #Add move diagonally to capture pieces if there is a piece to be captured
            if (self.position[0] + 1, self.position[1] + 1) in boardDict:
                if boardDict[(self.position[0] + 1, self.position[1] + 1)].blackwhite == "black":
                    validMoves.add((self.position[0] + 1, self.position[1] + 1))
            
            if (self.position[0] - 1, self.position[1] + 1) in boardDict:
                if boardDict[(self.position[0] - 1, self.position[1] + 1)].blackwhite == "black":
                    validMoves.add((self.position[0] - 1, self.position[1] + 1))

        elif self.blackwhite == "black":
            #Check if there is a piece in front of the pawn
            if (self.position[0], self.position[1] - 1) not in boardDict:
                validMoves.add((self.position[0], self.position[1] - 1))

                #Check to see if this is the first move the pawn has made. If so check to see if the pawn can move two spaces forward
                if self.position[1] == 6:
                    if (self.position[0], self.position[1] - 2) not in boardDict:
                        validMoves.add((self.position[0], self.position[1] - 2))
                
            #Add move diagonally to capture pieces if there is a piece to be captured
            if (self.position[0] + 1, self.position[1] - 1) in boardDict:
                if boardDict[(self.position[0] + 1, self.position[1] - 1)].blackwhite == "white":
                    validMoves.add((self.position[0] + 1, self.position[1] - 1))
            
            if (self.position[0] - 1, self.position[1] - 1) in boardDict:
                if boardDict[(self.position[0] - 1, self.position[1] - 1)].blackwhite == "white":
                    validMoves.add((self.position[0] - 1, self.position[1] - 1))

        return validMoves