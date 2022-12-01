from pieces.piece import Piece
from pieces.pawn import Pawn
from pieces.king import King
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.queen import Queen
from board_projection2 import project_board
from board_projection2 import extract_digit
from chessBoard import ChessBoard


from graphics.board import Board
from graphics.boardDisplay import BoardDisplay
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import cv2
import sys
import numpy as np
import tensorflow as tf

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

LETTER_DICT: dict = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J', 11: 'K', 12: 'L', 13: 'M', 14: 'N', 15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U', 22: 'V', 23: 'W', 24: 'X', 25: 'Y', 26: 'Z'}


#boardDict = {wr1.position: wr1, br2.position: br2}

#boardDict = {wb1.position: wb1, bb2.position: bb2}

#boardDict = {wkn1.position: wkn1, bkn1.position: bkn1}

#boardDict = {wk.position: wk, bk.position: bk}

board = ChessBoard(boardDict)

backgroundLocation = "chessBoardBlank.png"
boardDisplayer = BoardDisplay(backgroundLocation)
boardDisplayer.update(board.getBoardDict())

#graphicsBoard = Board(750, 750)

playing = True
turn = "white"


markerDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)

# marker1 = cv2.aruco.drawMarker(markerDict, 1, sidePixels=750)
# cv2.imshow("Marker 1", marker1)
#
# marker2 = cv2.aruco.drawMarker(markerDict, 2, sidePixels=750)
# cv2.imshow("Marker 2", marker2)
#
# cv2.imwrite("Marker1.png", marker1)
# cv2.imwrite("Marker2.png", marker2)


# Set up video capture from a USB camera
video_capture = cv2.VideoCapture(index=0)
got_img, bgr_img = video_capture.read()
if not got_img:
    print("Cannot read video source")
    sys.exit()

board_img = boardDisplayer.getDisplayImg()

while playing:
    got_img, bgr_img = video_capture.read()
    # Project the board onto the current image and show it
    projected_img, h, _ = project_board(bgr_img, board_img)
    cv2.imshow("Chess", projected_img)
    cv2.imshow("Board in 2D", board_img)
    cv2.imshow("Camera Feed", bgr_img)

    # print("Evaluation: ")
    # print(graphicsBoard.evaluate(boardDict))
    # boardDict = graphicsBoard.nextMove(boardDict, turn)
    # boardDisplayer.update(boardDict)
    # boardDisplayer.display()

    # Load letter and digit recognition models
    digit_model = tf.keras.models.load_model("digit_model.h5")
    letter_model = tf.keras.models.load_model("letter_model.h5")

    # Show the image for a millisecond, or exit the loop if a break key was pressed
    key_pressed = cv2.waitKey(1) & 0xFF
    if key_pressed == 27 or key_pressed == ord('q'):
        break
    elif key_pressed == ord('m'):
        startLocation = ['Z', -1]
        endLocation = ['X', -2]
        # for i in range(4):
        #     digit, success = extract_digit(bgr_img, i)
        #     if not success:
        #         print('Could not detect an ArUco marker, please try again')
        #         continue
        #     if i == 0:
        #         startLocation[0] = LETTER_DICT[np.argmax(letter_model.predict(digit.reshape(-1, 28, 28, 1)))]
        #     elif i == 1:
        #         startLocation[1] = np.argmax(digit_model.predict(digit.reshape(-1, 28, 28, 1)))
        #     elif i == 2:
        #         endLocation[0] = LETTER_DICT[np.argmax(letter_model.predict(digit.reshape(-1, 28, 28, 1)))]
        #     elif i == 3:
        #         endLocation[1] = np.argmax(digit_model.predict(digit.reshape(-1, 28, 28, 1)))
        #
        #
        #     if (i % 2):
        #         print(np.argmax(digit_model.predict(digit.reshape(-1, 28, 28, 1))))
        #     else:
        #         print(LETTER_DICT[np.argmax(letter_model.predict(digit.reshape(-1, 28, 28, 1)))])
        # print(startLocation)
        # print(endLocation)

        updatedBoard = board.movePiece(startLocation, endLocation, turn)

        #Code to use until cov net gets better
        if updatedBoard == False:
            updatedBoard = board.movePiece(['E', 2], ['E', 4], turn)


        if updatedBoard != False:

            boardDisplayer.update(board.getBoardDict())
            print(board.getBoardDict())
            board_img = boardDisplayer.getDisplayImg()
            cv2.imshow("Updated 2D board", board_img)
            if turn == "white":
              turn = "black"
            elif turn == "black":
              turn = "white"

