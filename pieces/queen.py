from .piece import Piece

class Queen(Piece):

    def __init__(self, position, blackwhite):
        super().__init__(position, blackwhite)
        self.img = 'none'
        if self.blackwhite == 'black':
            self.img = 'graphics/images/bq_11.png'
        elif self.blackwhite == 'white':
            self.img = 'graphics/images/wq_11.png'