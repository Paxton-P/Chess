from .piece import Piece

class Bishop(Piece):

    def __init__(self, position, blackwhite):
        super().__init__(position, blackwhite)
        self.img = 'none'
        if self.blackwhite == 'black':
            self.img = 'graphics/images/bb_11.png'
        elif self.blackwhite == 'white':
            self.img = 'graphics/images/wb_11.png'