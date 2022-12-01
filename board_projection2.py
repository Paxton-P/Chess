import cv2
import numpy as np
import math
import sys
import tensorflow as tf

# Camera parameter constants: will change based on the camera you're using
K: np.array = np.array([[1397.52735, 0, 652.871905], [0, 1397.20119, 332.295815], [0, 0, 1]], dtype=float)
DIST_COEFFS: np.array = np.array([[ .0952372421,  .246188134,  .00101888992, -.000459210685, -2.40973476]], dtype=float)

# Marker constants: Assuming the marker is 2in x 2in and comes from a 4x4 marker of 100
MARKER_SIZE: float = 2.0 #in
MARKER_DICT: dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)

# Chess board constants: bottom left corner of the board is just above and to the left of the marker, and the board will be 6inx6in
OFFSET: np.array = np.array([-1.0, -1.8, 0], dtype=float).reshape((1, 3))
WORLD_COORDS: np.array = np.array([(6, 0, 0), (6, 6, 0), (0, 6, 0), (0, 0, 0)], dtype=float)

# Letter constants that dictate the size of the image to extract and the offsets of the letters from the ArUco marker
LETTER_OFFSETS: np.array = np.array([(2.0, -1.0, 0), (4, -1.0, 0), (6.0, -1.0, 0), (8.5, -1.0, 0)])
LETTER_SIZE: float = 1.8 #in
DIGIT_COORDS: np.array = np.array([(0, 0, 0), (LETTER_SIZE, 0, 0), (LETTER_SIZE, LETTER_SIZE, 0), (0, LETTER_SIZE, 0)], dtype=float)

# Letter dictionary to convert from predictions to letters
LETTER_DICT: dict = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J', 11: 'K', 12: 'L', 13: 'M', 14: 'N', 15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U', 22: 'V', 23: 'W', 24: 'X', 25: 'Y', 26: 'Z'}

# List of mouse clicks to be used to detect where on the board has been clicked. Needs to be a global variable becuase I coun't figure it out any other way
mouse_clicks = []

def project_board(bgr_img: np.array, board_img: np.array) -> tuple((np.array, np.array, bool)):
    # Projects a chess board onto an image
    # Inputs:
    #   bgr_img: The image (hopefully containing an ArUco marker) to project the board onto
    #   board_img: The image of the board to project
    # Outputs:
    #   output_img: The image with the board on it if there is an ArUco marker, the original image if not
    #   h: The homography matrix found from board to image
    #   success: A boolean that is True if the board was successfully projected, and False if not

    # Define outputs
    output_img: np.array = bgr_img.copy()
    h: np.array = None
    success: bool = True
    
    # Find markers in image
    corners, ids, _ = cv2.aruco.detectMarkers(image=bgr_img, dictionary=MARKER_DICT)
    
    # If any were found, ...
    if ids is not None:
        # Get the pose of the marker
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners=corners, markerLength=MARKER_SIZE, cameraMatrix=K, distCoeffs=DIST_COEFFS)
        rvec_m_c = rvecs[0]
        tm_c = tvecs[0]

        # Construct rotation and translation vectos based on the pose of the marker
        last_row = np.array([0, 0, 0, 1], dtype=float).reshape((1, 4))       
        R_cm, _ = cv2.Rodrigues(rvec_m_c)
        H_cm = np.concatenate((R_cm, tm_c.T), axis=1)
        H_cm = np.concatenate((H_cm, last_row), axis=0)

        R_mo, _ = cv2.Rodrigues(np.array([0, 0, -math.pi/2], dtype=float))
        H_mo = np.concatenate((R_mo, OFFSET.T), axis=1)
        H_mo = np.concatenate((H_mo, last_row), axis=0)

        H_co = np.matmul(H_cm, H_mo)
        rvec, _ = cv2.Rodrigues(H_co[:3, :3])
        tvec = H_co[:3, 3]

        # Project the corners of the board onto the image
        img_pts, _ = cv2.projectPoints(objectPoints=WORLD_COORDS, rvec=rvec, tvec=tvec, cameraMatrix=K, distCoeffs=DIST_COEFFS)
        img_pts = img_pts.round(0).astype(int)

        # Define corners of the board image to contian the entire image
        board_pts: np.array = np.array([(board_img.shape[1], board_img.shape[0]), (0, board_img.shape[0]), (0, 0), (board_img.shape[1], 0)], dtype=float)

        # Find a homography between the corners of the board image and the corners in bgr_img
        h, _ = cv2.findHomography(board_pts, img_pts)

        # Warp the board according to that homography and put it on the output image
        warped_board: np.array = cv2.warpPerspective(board_img, h, (bgr_img.shape[1], bgr_img.shape[0]))
        bgr_img: np.array = cv2.fillConvexPoly(bgr_img, img_pts, (0, 0, 0))
        output_img = bgr_img + warped_board
    # If we don't detect any ArUco markers, print that to console and set success equal to false
    else:
        # print('No ArUco markers detected')
        success = False

    # return the outputs
    return (output_img, h, success)

def coords_to_square(board_img: np.array, board_coords: tuple((int, int))) -> tuple((str, bool)):
    # Takes a position on the board and gets the corresponding chess board square
    # Inputs:
    #   board_img: The image of the board, used to get the height and width in pixels
    #   board_coords: A tuple of pixel locations on the board, as returned by a mouse callback function
    # Output:
    #   square: A string representing the square on the board, e.g. A1
    #   success: A bool representing whether the click was on the board

    # Determing th height and width of the board image in pixels
    h: int = board_img.shape[0]
    w: int = board_img.shape[1]

    # Normalize the coordinates to be a proportion of horizontal and vertical
    v_norm: float = board_coords[1]/h
    h_norm: float = board_coords[0]/w

    # Get the horizontal portion of the square (A-H)
    chr_1: str
    if h_norm < 0.125  : chr_1 = 'A'
    elif h_norm < 0.25 : chr_1 = 'B'
    elif h_norm < 0.375: chr_1 = 'C'
    elif h_norm < 0.5  : chr_1 = 'D'
    elif h_norm < 0.625: chr_1 = 'E'
    elif h_norm < 0.75 : chr_1 = 'F'
    elif h_norm < 0.875: chr_1 = 'G'
    elif h_norm <= 1   : chr_1 = 'H'
    else: 
        chr_1 = 'Z'
        success = False

    # Get the vertical portion of the square (1-8)
    chr_2: str
    if v_norm < 0.125  : chr_2 = '8'
    elif v_norm < 0.25 : chr_2 = '7'
    elif v_norm < 0.375: chr_2 = '6'
    elif v_norm < 0.5  : chr_2 = '5'
    elif v_norm < 0.625: chr_2 = '4'
    elif v_norm < 0.75 : chr_2 = '3'
    elif v_norm < 0.875: chr_2 = '2'
    elif v_norm <= 1   : chr_2 = '1'
    else: 
        chr_2 = '0'
        success = False

    # Combine chr_1 and chr_2 and return the result
    square: str = chr_1 + chr_2

    return (square, success)

def get_xy(event, x, y, flags, param):
    # Appends the x and y coordinate of a left click to mouse_clicks
    # Inputs:
    #   event: The event type, the only one we care about is left mouse click
    #   x: The x coordinate of the event
    #   y: The y coordinate of the event
    #   flags: Unimportant
    #   params: Unimportant
    # Outputs: None

    global mouse_clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_clicks.append((x, y))

def image_to_board(img_pt: tuple((int, int)), h: np.array) -> tuple:
    # Transforms image coordinates to board coordinates
    # Inputs:
    #   image_pt: The coordinates of the point in the image, as stored in mouse_clicks
    #   h: A homography from the board to the image, as calculated by project_board
    # Outputs:
    #   board_pt: The coordinates of the point in the board image

    # Find inverse of h, which will be the homography from the image to the board
    h_inv: np.array = np.linalg.inv(h)

    # Convert the image point to homogeneous coordinates, transform it to the board, and convert back to (x, y)
    img_pt_h = np.array([img_pt[0], img_pt[1], 1], dtype=float).reshape((3, 1))
    board_pt_h: np.array = h_inv @ img_pt_h
    board_pt: tuple = (board_pt_h[0], board_pt_h[1])

    return board_pt
        
def extract_digit(img: np.array, index: int) -> tuple((np.array, bool)):
    # Extracts an image of a digit from the whiteboard
    # Inputs:
    #   img: The image of the whiteboard to extract from
    #   index: The index of the digit to extract (1 - 4)
    # Ouputs:
    #   output: An image of the digit
    #   success: A boolean that is False if there were no ArUco markers and True if there was at least 1

    corners, ids, _ = cv2.aruco.detectMarkers(image=img, dictionary=MARKER_DICT)
    output = None
    success: bool = False

    if ids is not None:  

        success = True  

        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners=corners, markerLength=MARKER_SIZE, cameraMatrix=K, distCoeffs=DIST_COEFFS)
        rvec_m_c = rvecs[0]
        tm_c = tvecs[0]

        last_row = np.array([0, 0, 0, 1], dtype=float).reshape((1, 4))       
        R_cm, _ = cv2.Rodrigues(rvec_m_c)
        H_cm = np.concatenate((R_cm, tm_c.T), axis=1)
        H_cm = np.concatenate((H_cm, last_row), axis=0)
        R_mo, _ = cv2.Rodrigues(np.array([0, 0, 0], dtype=float))
        H_mo = np.concatenate((R_mo, (LETTER_OFFSETS[index]).reshape((1, 3)).T), axis=1)
        H_mo = np.concatenate((H_mo, last_row), axis=0)

        H_co = np.matmul(H_cm, H_mo)
        rvec, _ = cv2.Rodrigues(H_co[:3, :3])
        tvec = H_co[:3, 3]

        img_pts, _ = cv2.projectPoints(objectPoints=DIGIT_COORDS, rvec=rvec, tvec=tvec, cameraMatrix=K, distCoeffs=DIST_COEFFS)

        output_shape: tuple = (128, 128)
        output_pts: np.array = np.array([(0, 0), (0, output_shape[0]), (output_shape[1], output_shape[0]), (output_shape[1], 0)], dtype=float)

        h, _ = cv2.findHomography(img_pts, output_pts)

        digit_img = cv2.rotate(cv2.warpPerspective(img, h, (output_shape[1], output_shape[0])), cv2.ROTATE_90_COUNTERCLOCKWISE)
        grey_digit = cv2.cvtColor(digit_img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(grey_digit, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 111, 20)
        # cv2.imshow("test", thresh)
        # cv2.waitKey(0)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        biggest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(biggest_contour)
        just_digit = cv2.resize(thresh[y:y+h, x:x+w], (18, 18))
        # cv2.imshow("test", cv2.rectangle(digit_img, (x, y), (x+w, y+h), color=(0, 0, 255), thickness=1))
        # cv2.waitKey(0)
        output = np.pad(just_digit, ((5, 5), (5, 5)), "constant", constant_values=0)
        

    
    return (output, success)
def main() -> None:

    # Define board_img to be a starting board, will need to change this later
    board_img: np.array = cv2.imread('chess_board.png')
    
    # Set up video capture from a USB camera
    video_capture = cv2.VideoCapture(index=0)
    got_img, bgr_img = video_capture.read()
    if not got_img:
        print("Cannot read video source")
        sys.exit()

    # Load letter and digit recognition models
    digit_model = tf.keras.models.load_model('digit_model.h5')
    letter_model = tf.keras.models.load_model('letter_model.h5')
    
    # Continually read in the video feed until esc or q is pressed
    while True:
        got_img, bgr_img = video_capture.read()

        # Project the board onto the current image and show it
        projected_img, h, _ = project_board(bgr_img, board_img)
        cv2.imshow("test", projected_img)

        # Get locations of mouse click and store them in mouse_clicks
        # cv2.setMouseCallback("test", get_xy, param=mouse_clicks)

        # Temporarily just print the square to console, later will need to integrate this into the chess engine
        # if(len(mouse_clicks) != 0):
        #     x, y = mouse_clicks.pop(0)
        #     board_coords = image_to_board(img_pt=(x, y), h=h)
        #     print(coords_to_square(board_img, board_coords))

        # Show the image for a millisecond, or exit the loop if a break key was pressed
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            break
        elif key_pressed == ord('m'):
            for i in range(4):
                digit, success = extract_digit(bgr_img, i)
                if not success:
                    print('Could not detect an ArUco marker, please try again')
                    continue
                if(i % 2):
                    print(np.argmax(digit_model.predict(digit.reshape(-1, 28, 28, 1))))
                else:
                    print(LETTER_DICT[np.argmax(letter_model.predict(digit.reshape(-1, 28, 28, 1)))])
    

    

if __name__ == "__main__":
    main()
