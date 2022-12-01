import cv2
import numpy as np

class BoardDisplay:
    background = None

    def __init__(self, boardImageLoc):
        boardImageBGR = cv2.imread(boardImageLoc)
        boardImageBGR = cv2.resize(boardImageBGR, dsize=(750, 750))

        self.img = boardImageBGR
        self.width = boardImageBGR.shape[1]
        self.height = boardImageBGR.shape[0]
        
        ones = np.ones((self.height, self.width))*255
        boardImageBGR = np.dstack([boardImageBGR, ones])
        self.img = boardImageBGR
        BoardDisplay.background = boardImageBGR
        self.boardImageLoc = boardImageLoc
        print("in here")
    
    def update(self, boardDict):
        boardImageBGR = cv2.imread(self.boardImageLoc)
        boardImageBGR = cv2.resize(boardImageBGR, dsize=(750, 750))
        ones = np.ones((self.height, self.width))*255
        boardImageBGR = np.dstack([boardImageBGR, ones])

        self.img = boardImageBGR

        print(boardDict)

        #self.img = BoardDisplay.background

        cv2.imshow("Background", self.img.astype(np.uint8))



        for pieceLoc in boardDict:
            piece = boardDict[pieceLoc]

            inImageLoc = (int((7 - piece.position[1]) * self.width/8 + self.width/8/2), int((piece.position[0]) * self.height/8 + self.height/8/2))
            pieceImgName = piece.img
            
            pieceImg = cv2.imread(pieceImgName, cv2.IMREAD_UNCHANGED)
            pieceHeight = pieceImg.shape[0]
            pieceWidth = pieceImg.shape[1]

            alpha_image_3 = pieceImg[:, :, 3] / 255.0
            alpha_image = 1 - alpha_image_3

            for c in range(0, 3):
                cutOut = (alpha_image_3*pieceImg[:, :, c])
                y1 = int(inImageLoc[0] - pieceHeight/2)
                y2 = int(pieceHeight/2 + inImageLoc[0])
                x1 = int(inImageLoc[1] - pieceWidth/2)
                x2 = int(pieceWidth/2 + inImageLoc[1])

                backgroundImg = (alpha_image*self.img[y1:y2, x1:x2, c])

                overlayedImg = (backgroundImg + cutOut)
                self.img[y1:y2, x1:x2, c] = overlayedImg

    def display(self):
        cv2.imshow("Board Image",self.img.astype(np.uint8))

