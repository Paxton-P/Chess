import cv2
import numpy as np
import math
import sys
import tensorflow as tf

# Camera parameter constants: will change based on the camera you're using
K: np.array = np.array([[1397.52735, 0, 652.871905], [0, 1397.20119, 332.295815], [0, 0, 1]], dtype=float)
DIST_COEFFS: np.array = np.array([[.0952372421,  .246188134,  .00101888992, -.000459210685, -2.40973476]], dtype=float)

# Marker constants: Assuming the marker is 2in x 2in and comes from a 4x4 marker of 100
MARKER_SIZE: float = 2.0 #in
MARKER_DICT: dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)

# Chess board constants: bottom left corner of the board is just above and to the left of the marker, and the board will be 6inx6in
OFFSET: np.array = np.array([-1.0, -1.8, 0], dtype=float).reshape((1, 3))
WORLD_COORDS: np.array = np.array([(6, 0, 0), (6, 6, 0), (0, 6, 0), (0, 0, 0)], dtype=float)

# Letter constants that dictate the size of the image to extract and the offsets of the letters from the ArUco marker
LETTER_OFFSETS: np.array = np.array([(2.0, -1.0, 0), (4.5, -1.0, 0), (6.25, -1.0, 0), (8.75, -1.0, 0)])
LETTER_SIZE: float = 1.8 #in
DIGIT_COORDS: np.array = np.array([(0, 0, 0), (LETTER_SIZE, 0, 0), (LETTER_SIZE, LETTER_SIZE, 0), (0, LETTER_SIZE, 0)], dtype=float)

# Letter dictionary to convert from predictions to letters
LETTER_DICT: dict = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H'}


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
        
def extract_digit(img: np.array, index: int) -> tuple((np.array, bool)):
    # Extracts an image of a digit from the whiteboard
    # Inputs:
    #   img: The image of the whiteboard to extract from
    #   index: The index of the digit to extract (1 - 4)
    # Ouputs:
    #   output: An image of the digit
    #   success: A boolean that is False if there were no ArUco markers and True if there was at least 1

    # Find ArUco markers in the image and set up output variables
    corners, ids, _ = cv2.aruco.detectMarkers(image=img, dictionary=MARKER_DICT)
    output = None
    success: bool = False

    if ids is not None:  

        # If we found an ArUco markey, success = True
        success = True  

        # Get the pose of the found marker
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners=corners, markerLength=MARKER_SIZE, cameraMatrix=K, distCoeffs=DIST_COEFFS)
        rvec_m_c = rvecs[0]
        tm_c = tvecs[0]

        # Perform operations to find a homography between the camera and the desired segment of the whiteboard
        last_row = np.array([0, 0, 0, 1], dtype=float).reshape((1, 4))       
        R_cm, _ = cv2.Rodrigues(rvec_m_c)
        H_cm = np.concatenate((R_cm, tm_c.T), axis=1)
        H_cm = np.concatenate((H_cm, last_row), axis=0)
        R_mo, _ = cv2.Rodrigues(np.array([0, 0, 0], dtype=float))
        H_mo = np.concatenate((R_mo, (LETTER_OFFSETS[index]).reshape((1, 3)).T), axis=1)
        H_mo = np.concatenate((H_mo, last_row), axis=0)
        H_co = np.matmul(H_cm, H_mo)

        # Use this homography matrix to find the rotation and translation vectors that cv2.ProjectPoints expects
        rvec, _ = cv2.Rodrigues(H_co[:3, :3])
        tvec = H_co[:3, 3]

        # Get the corners of the desired segment of the whiteboard in image coordinates
        img_pts, _ = cv2.projectPoints(objectPoints=DIGIT_COORDS, rvec=rvec, tvec=tvec, cameraMatrix=K, distCoeffs=DIST_COEFFS)

        # Define what we want our output points to be (the corners of a 128 by 128 image)
        output_shape: tuple = (128, 128)
        output_pts: np.array = np.array([(0, 0), (0, output_shape[0]), (output_shape[1], output_shape[0]), (output_shape[1], 0)], dtype=float)

        # Find a homography between the image and output points
        h, _ = cv2.findHomography(img_pts, output_pts)

        # Extract just the image of the digit using the found homography, convert it to greyscale, and use adaptive thresholding to convert it to binary
        digit_img = cv2.rotate(cv2.warpPerspective(img, h, (output_shape[1], output_shape[0])), cv2.ROTATE_90_COUNTERCLOCKWISE)
        grey_digit = cv2.cvtColor(digit_img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(grey_digit, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 111, 20)

        # Find the contours of the binary image and store the largest one by area as what we think our digit is
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        biggest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(biggest_contour)

        # Extract that contour from the thresholded image, resize and pad it with zeros to match the format of the MNIST dataset (what our CNNs were trained on)
        just_digit = cv2.resize(thresh[y:y+h, x:x+w], (18, 18))
        output = np.pad(just_digit, ((5, 5), (5, 5)), "constant", constant_values=0)
        
    return (output, success)


def main() -> None:

    # Define board_img to be a starting board for testing purposes
    board_img: np.array = cv2.imread('chess_board.png')
    
    # Set up video capture from a USB camera
    video_capture = cv2.VideoCapture(index=0)
    got_img, bgr_img = video_capture.read()
    if not got_img:
        print("Cannot read video source")
        sys.exit()

    # Load letter and digit recognition models
    digit_model = tf.keras.models.load_model("digit_model.h5")
    letter_model = tf.keras.models.load_model("letter_model.h5")
    
    # Continually read in the video feed until esc or q is pressed
    while True:
        got_img, bgr_img = video_capture.read()

        # Project the board onto the current image and show it
        projected_img, h, _ = project_board(bgr_img, board_img)
        cv2.imshow("test", projected_img)

        # Show the image for a millisecond, or exit the loop if a break key was pressed
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            break

        # Print out letter and digit predictions for testing purposes
        elif key_pressed == ord('m'):
            for i in range(4):
                digit, success = extract_digit(bgr_img, i)
                if not success:
                    print('Could not detect an ArUco marker, please try again')
                    continue
                if(i % 2):
                    print(np.argmax(digit_model.predict(digit.reshape(-1, 28, 28, 1))[0, 1:9]) + 1)
                else:
                    print(LETTER_DICT[np.argmax(letter_model.predict(digit.reshape(-1, 28, 28, 1))[0, 1:9]) + 1])
    

    

if __name__ == "__main__":
    main()
