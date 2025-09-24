import numpy as np
import cv2 as cv
import glob
from pathlib import Path


# Stworz folder na zdjęcia jeśli nie istnieje, jak istnieje to ignoruj
Path("./cal_images").mkdir(exist_ok = True)

cam = cv.VideoCapture(0)

# Get min 10 images
img_count = 0
print("Wykonaj min 10 zdjec")
print('Naciśnij "c" aby zrobic zdjecie')
print('Nacisnij "q" aby zakonczyc robienie zdjec')
while True:
    ret, frame = cam.read()
    if not ret:
        print("Błąd odczytu klatki")
        break
    
    r = cv.resize(frame, (267, 200))
    cv.imshow('podglad', r)
    # print('Ilosc wykonanych do tej pory zdjec: {}'.format(img_count))
    k = cv.waitKey(1)
    
    if k == ord('q'):
        print('Nacisnieto "q", konczenie wykonywania zdjec...')
        break
    elif k == ord('c'):
        img_name = "./cal_images/cal_test_{}.jpg".format(img_count)
        cv.imwrite(img_name, frame)
        print("zapisano {}".format(img_name))
        img_count += 1

cam.release()
cv.destroyAllWindows()    



# terminate criteria
criteria =(cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0), ..., (6,5,0)
objp = np.zeros((6*7, 3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane

images = glob.glob('./cal_images/*.jpg')
# images = glob.glob('./left/*.jpg')
# print(images)

for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    # Find the chessboard corners
    ret, corners = cv.findChessboardCorners(gray, (7,6), None)
    
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        
        corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)
        
        # Draw and display the corners
        cv.drawChessboardCorners(img, (7,6), corners2, ret)
        r_img = cv.resize(img, (800, 600))
        cv.imshow('img', r_img)
        cv.waitKey(500)
        
cv.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# img = cv.imread('./left/left12.jpg')
img = cv.imread('./cal_images/cal_test_0.jpg')
h, w = img.shape[:2]
new_cam_mtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 0, (w,h))

# undistort
dst = cv.undistort(img, mtx, dist, None, new_cam_mtx)

# crop the image
x, y, w, h = roi
print(roi)
dst = dst[y:y+h, x:x+w]
cv.imwrite('calibres.png', dst)
print('undistorted')