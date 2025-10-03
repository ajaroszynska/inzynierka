import cv2
from zapisz_n_zdjec import *

print("szachownica")
n_zdjec = 15
sciezka_zapisu = "./test_img/cal_img/"
zapisz_n_zdjec(n_zdjec, sciezka_zapisu, "chessboard_", 0)

print("klocki")
n_zdjec = 9
sciezka_zapisu = "./test_img/cal_img/"
zapisz_n_zdjec(n_zdjec, sciezka_zapisu, "object_", 1)