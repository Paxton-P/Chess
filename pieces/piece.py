class Piece:
    value = 0

    def __init__(self, position, blackwhite):
        self.position = position
        self.alive = True
        self.blackwhite = blackwhite

    def capture(self):
        self.alive = False

    def move(self, position):
        self.position = position

    def printPiece(self):
        print("Piece")
    
    def __str__(self):
        return "Piece: " + self.blackwhite + " (" + str(self.position[0]) + "," + str(self.position[1]) + ")"

    def findValidMoves(self):
        return

    def validPos(posistion):
        if posistion[0] <= 7 and posistion[0] >= 0 and posistion[1] <= 7 and posistion[1] >= 0:
            return True
        else:
            return False
            
