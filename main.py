from pieces.piece import Piece
from pieces.pawn import Pawn
from pieces.king import King
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.queen import Queen

from graphics.board import Board
from graphics.boardDisplay import BoardDisplay
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import cv2

#Black Pieces
bp1 = Pawn((0,6),"black")
bp2 = Pawn((1,6),"black")
bp3 = Pawn((2,6),"black")
bp4 = Pawn((3,6),"black")
bp5 = Pawn((4,6),"black")
bp6 = Pawn((5,6),"black")
bp7 = Pawn((6,6),"black")
bp8 = Pawn((7,6),"black")

bk = King((4,7), "black")
bq = Queen((3,7), "black")

br1 = Rook((0,7), "black")
br2 = Rook((7,7), "black")

bb1 = Bishop((2,7), "black")
bb2 = Bishop((5,7), "black")

bkn1 = Knight((1,7), "black")
bkn2 = Knight((6,7), "black")

#White Pieces
wp1 = Pawn((0,1),"white")
wp2 = Pawn((1,1),"white")
wp3 = Pawn((2,1),"white")
wp4 = Pawn((3,1),"white")
wp5 = Pawn((4,1),"white")
wp6 = Pawn((5,1),"white")
wp7 = Pawn((6,1),"white")
wp8 = Pawn((7,1),"white")

wk = King((4,0), "white")
wq = Queen((3,0), "white")

wr1 = Rook((0,0), "white")
wr2 = Rook((7,0), "white")

wb1 = Bishop((2,0), "white")
wb2 = Bishop((5,0), "white")

wkn1 = Knight((1,0), "white")
wkn2 = Knight((6,0), "white")

boardDict = {wp1.position: wp1, wp2.position: wp2, wp3.position: wp3, wp4.position: wp4, wp5.position: wp5, wp6.position: wp6, wp7.position: wp7, wp8.position: wp8,
             bp1.position: bp1, bp2.position: bp2, bp3.position: bp3, bp4.position: bp4, bp5.position: bp5, bp6.position: bp6, bp7.position: bp7, bp8.position: bp8,
             wr1.position: wr1, wr2.position: wr2, br1.position: br1, br2.position: br2, wb1.position: wb1, wb2.position: wb2, bb1.position: bb1, bb2.position: bb2,
             wkn1.position: wkn1, wkn2.position: wkn2, bkn1.position: bkn1, bkn2.position: bkn2, wk.position: wk, bk.position: bk,
             wq.position: wq, bq.position: bq}

#boardDict = {wr1.position: wr1, br2.position: br2}

#boardDict = {wb1.position: wb1, bb2.position: bb2}

#boardDict = {wkn1.position: wkn1, bkn1.position: bkn1}

#boardDict = {wk.position: wk, bk.position: bk}

#boardDict = {}

backgroundLocation = "chessBoardBlank.png"
boardDisplayer = BoardDisplay(backgroundLocation)

boardDisplayer.display()

boardDisplayer.update(boardDict)

boardDisplayer.display()


graphicsBoard = Board(750,750)

playing = True
turn = "white"

while playing:
   print("Evaluation: ")
   print(graphicsBoard.evaluate(boardDict))
   boardDict = graphicsBoard.nextMove(boardDict, turn)
   boardDisplayer.update(boardDict)
   boardDisplayer.display()
   if turn == "white":
      turn = "black"
   elif turn == "black":
      turn = "white"


#chessBoard.drawBoard([bp1, bp2, bp3, bp4, bp5, bp6, bp7, bp8, bk, bq, br1, br2, bb1, bb2, bkn1, bkn2,
#                      wp1, wp2, wp3, wp4, wp5, wp6, wp7, wp8, wk, wq, wr1, wr2, wb1, wb2, wkn1, wkn2])