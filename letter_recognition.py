import cv2
import numpy as np
import math

# Camera parameter constants: will change based on the camera you're using
K: np.array = np.array([[1397.52735, 0, 652.871905], [0, 1397.20119, 332.295815], [0, 0, 1]], dtype=float)
DIST_COEFFS: np.array = np.array([[ .0952372421,  .246188134,  .00101888992, -.000459210685, -2.40973476]], dtype=float)

# ArUco constants: assumes the markers are 2in x 2in and come from a 4X4 dictionary with 100 markers
MARKER_SIZE: float = 2.0 #in
MARKER_DICT: dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)

# Letter constants that dictate the size of the image to extract and the offsets of the letters from the ArUco marker
LETTER_OFFSETS: np.array = np.array([(2.15, -0.9, 0), (4.3, -0.9, 0), (6.3, -0.9, 0), (8.25, -0.9, 0)])
LETTER_SIZE: float = 1.8 #in
WORLD_COORDS: np.array = np.array([(0, 0, 0), (LETTER_SIZE, 0, 0), (LETTER_SIZE, LETTER_SIZE, 0), (0, LETTER_SIZE, 0)], dtype=float)

def extract_digit(img: np.array, index: int) -> tuple((np.array, bool)):
    # Extracts an image of a digit from the whiteboard
    # Inputs:
    #   img: The image of the whiteboard to extract from
    #   index: The index of the digit to extract (1 - 4)
    # Ouputs:
    #   output: An image of the digit
    #   success: A boolean that is Falso if there were no ArUco markers and True if there was at least 1

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

        img_pts, _ = cv2.projectPoints(objectPoints=WORLD_COORDS, rvec=rvec, tvec=tvec, cameraMatrix=K, distCoeffs=DIST_COEFFS)

        output_shape: tuple = (128, 128)
        output_pts: np.array = np.array([(0, 0), (0, output_shape[0]), (output_shape[1], output_shape[0]), (output_shape[1], 0)], dtype=float)

        h, _ = cv2.findHomography(img_pts, output_pts)

        output_image = cv2.rotate(cv2.warpPerspective(img, h, (output_shape[1], output_shape[0])), cv2.ROTATE_90_COUNTERCLOCKWISE)
        print(output_image.shape)

        output = output_image
    
    return (output, success)

            

def main() -> None:

    # Test the function: reads in the test image and displays the digits
    test_img: np.array = cv2.imread('example.jpg')
    for i in range(4):
        test, _ = extract_digit(test_img, i)
        cv2.imshow("test", test)
        cv2.waitKey(0)
    

if __name__ == "__main__":
    main()