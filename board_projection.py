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

def project_board(bgr_img: np.array, board_img: np.array) -> tuple((np.array, bool)):
    # Projects a chess board onto an image
    # Inputs:
    #   bgr_img: The image (hopefully containing an ArUco marker) to project the board onto
    #   board_img: The image of the board to project
    # Outputs:
    #   output_img: The image with the board on it if there is an ArUco marker, the original image if not
    #   success: A boolean that is True if the board was successfully projected, and False if not

    # Define outputs
    output_img: np.array = bgr_img.copy()
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
        print('No ArUco markers detected')
        success = False

    # return the outputs
    return (output_img, success)

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
        projected_img, _ = project_board(bgr_img, board_img)
        cv2.imshow("test", projected_img)

        # Show the image for a millisecond, or exit the loop if a break key was pressed
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            break


if __name__ == "__main__":
    main()
