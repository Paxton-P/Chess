class Piece:
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
