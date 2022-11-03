from .piece import Piece

class King(Piece):

    def __init__(self, position, blackwhite):
        super().__init__(position, blackwhite)
        self.img = 'none'
        if self.blackwhite == 'black':
            self.img = 'graphics/images/bk_6_11.png'
        elif self.blackwhite == 'white':
            self.img = 'graphics/images/wk_11.png'