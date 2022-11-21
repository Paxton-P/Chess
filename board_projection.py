import cv2
import numpy as np
import math
import sys

# Camera parameter constants: will change based on the camera you're using
K: np.array = np.array([[1397.52735, 0, 652.871905], [0, 1397.20119, 332.295815], [0, 0, 1]], dtype=float)
DIST_COEFFS: np.array = np.array([[ .0952372421,  .246188134,  .00101888992, -.000459210685, -2.40973476]], dtype=float)

# Marker constants: Assuming the marker is 2in x 2in and comes from a 4x4 marker of 100
MARKER_SIZE: float = 2.0 #in
MARKER_DICT: dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)

# Chess board constants: bottom left corner of the board is just above and to the left of the marker, and the board will be 6inx6in
OFFSET: np.array = np.array([-1.5, 1.5, 0], dtype=float).reshape((1, 3))
WORLD_COORDS: np.array = np.array([(0, 0, 0), (0, -6, 0), (-6, -6, 0), (-6, 0, 0)], dtype=float)

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
        img_pts, _ = cv2.projectPoints(objectPoints=WORLD_COORDS, rvec=rvec, tvec=tvec, cameraMatrix=K, distCoeffs=None)
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

def coords_to_square(board_img: np.array, board_coords: tuple((int, int))) -> str:
    # Takes a position on the board and gets the corresponding chess board square
    # Inputs:
    #   board_img: The image of the board, used to get the height and width in pixels
    #   board_coords: A tuple of pixel locations on the board, as returned by a mouse callback function
    # Output:
    #   square: A string representing the square on the board, e.g. A1

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
    else: chr_1 = 'Z'

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
    else: chr_2 = '0'

    # Combine chr_1 and chr_2 and return the result
    square: str = chr_1 + chr_2

    return square

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
        


def main() -> None:

    # Define board_img to be a starting board, will need to change this later
    board_img: np.array = cv2.imread('chess_board.png')
    
    # Set up video capture from a USB camera
    video_capture = cv2.VideoCapture(index=0)
    got_img, bgr_img = video_capture.read()
    if not got_img:
        print("Cannot read video source")
        sys.exit()
    
    # Continually read in the video feed until esc or q is pressed
    while True:
        got_img, bgr_img = video_capture.read()

        # Project the board onto the current image and show it
        projected_img, h, _ = project_board(bgr_img, board_img)
        cv2.imshow("test", projected_img)

        # Get locations of mouse click and store them in mouse_clicks
        cv2.setMouseCallback("test", get_xy, param=mouse_clicks)

        # Temporarily just print the square to console, later will need to integrate this into the chess engine
        if(len(mouse_clicks) != 0):
            x, y = mouse_clicks.pop(0)
            board_coords = image_to_board(img_pt=(x, y), h=h)
            print(coords_to_square(board_img, board_coords))

        # Show the image for a millisecond, or exit the loop if a break key was pressed
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            break    

if __name__ == "__main__":
    main()
