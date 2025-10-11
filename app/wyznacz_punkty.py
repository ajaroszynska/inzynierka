import cv2
import numpy as np

def wyznacz_punkty(n_punktow, m_wymiarow, pdq):
    c = cv2.VideoCapture(0)
    while True:
        _, zdj = c.read()
        # zdj = cv2.imread('D:\\studia\\inzynierka\\app\\test_img\\cal_img\\chessboard_0.jpg')

        for i in range(0, n_punktow):
                p_wsp = tuple(pdq[i])
                zdj = cv2.circle(zdj, p_wsp, radius=20, color=(0, 0, 255), thickness=-1)
        
        # r = cv2.resize(zdj, (640, 480))


        
        cv2.imshow('okienko', zdj)
        if cv2.waitKey(1)==ord("q"):
            break
                
    cv2.destroyAllWindows()
    return
    
    