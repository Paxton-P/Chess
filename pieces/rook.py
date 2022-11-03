from .piece import Piece

class Rook(Piece):

    def __init__(self, position, blackwhite):
        super().__init__(position, blackwhite)
        self.img = 'none'
        if self.blackwhite == 'black':
            self.img = 'graphics/images/br_11.png'
        elif self.blackwhite == 'white':
            self.img = 'graphics/images/wr_11.png'