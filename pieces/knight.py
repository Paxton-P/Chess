from .piece import Piece

class Knight(Piece):

    def __init__(self, position, blackwhite):
        super().__init__(position, blackwhite)
        self.img = 'none'
        if self.blackwhite == 'black':
            self.img = 'graphics/images/bkn_11.png'
        elif self.blackwhite == 'white':
            self.img = 'graphics/images/wkn_11.png'