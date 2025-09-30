import cv2
import numpy as np
# import glob

def wsp_znieksztalcenia(zdjecia, sciezka, wymiar1=8, wymiar2=5):
    # terminate criteria
    criteria =(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0), ..., (6,5,0)
    objp = np.zeros((wymiar2*wymiar1, 3), np.float32)
    objp[:,:2] = np.mgrid[0:wymiar1,0:wymiar2].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images
    obj_punkty = [] # 3d point in real world space
    zdj_punkty = [] # 2d points in image plane

    # images = glob.glob('./cal_images/*.jpg')
    # zdjecia_k = glob.glob( "D:\\studia\\inzynierka\\test_kamerki\\left\\*.jpg")
    # zdjecia = glob.glob("D:\\studia\\inzynierka\\test_kamerki\\cal_images\\*.jpg")
    # print(images)

    for zdj_nazwa in zdjecia:
        zdj = cv2.imread(zdj_nazwa)
        gray = cv2.cvtColor(zdj, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, wierzcholki = cv2.findChessboardCorners(gray, (wymiar1,wymiar2), None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            obj_punkty.append(objp)

            wierzcholki2 = cv2.cornerSubPix(gray, wierzcholki, (11,11), (-1,-1), criteria)
            zdj_punkty.append(wierzcholki2)

            # Draw and display the corners
            cv2.drawChessboardCorners(zdj, (wymiar1,wymiar2), wierzcholki2, ret)
            r_zdj = cv2.resize(zdj, (800, 600))
            cv2.imshow('zdj', r_zdj)
            cv2.waitKey(500)

    cv2.destroyAllWindows()

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_punkty, zdj_punkty, gray.shape[::-1], None, None)
    print("mtx:")
    print(mtx)
    print("dist:")
    print(dist)

    

    # img = cv2.imread('./left/left12.jpg')
    zdj = cv2.imread(zdjecia[0])
    h, w = zdj.shape[:2]
    new_cam_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 0, (w,h))
    print("new_mtx:")
    print(new_cam_mtx)

    new_mtxs = []

    for zdjn in zdjecia:
        zdj = cv2.imread(zdjn)
        h, w = zdj.shape[:2]
        new_cam_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 0, (w,h))
        new_mtxs.append(new_cam_mtx)
        print(new_cam_mtx)
    
    print("\n\n\n")
    print("old")
    print(mtx)
    print("1st")
    print(new_mtxs[0])
    print("last")
    print(new_mtxs[-1])
    print("average")
    avg_new_mtx = np.zeros((3,3), np.float64)
    for m in new_mtxs:
        avg_new_mtx[0][0] += m[0][0]
        avg_new_mtx[0][1] += m[0][1]
        avg_new_mtx[0][2] += m[0][2]
        avg_new_mtx[1][2] += m[1][0]
        avg_new_mtx[1][1] += m[1][1]
        avg_new_mtx[1][0] += m[1][2]
        avg_new_mtx[2][0] += m[2][0]
        avg_new_mtx[2][1] += m[2][1]
        avg_new_mtx[2][2] += m[2][2]
    
    avg_new_mtx = np.divide(avg_new_mtx, len(new_mtxs))
    print(avg_new_mtx)


    #return mtx, dist, new_cam_mtx

    # # undistort
    # dst = cv2.undistort(zdj, mtx, dist, None, new_cam_mtx)

    # # crop the image
    # x, y, w, h = roi
    # print(roi)
    # dst = dst[y:y+h, x:x+w]
    # cv2.imwrite(sciezka + 'calibres.png', dst)
    # print('undistorted')
    
    return