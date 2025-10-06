import cv2
import glob
from zapisz_n_zdjec import *
from wsp_znieksztalcenia import *
from detekcja_ksztaltu import *

# Skrypt kalibracji kamery

# Wyznacz współczynniki zniekształcenia i macierz kamery
# Zrób min. 10 zdjęć z szachownicą w różnych pozycjach
# Szachownica musi być asymetryczna, np. 8x5; 5x5 nie zadziała!
# n_zdjec = int(input("Podaj liczbe zdjec do wyznaczenia wsp znieksztalcenia (min. 10): "))
sciezka_zapisu = ".\\test_img\\cal_img\\" # placeholder - w linuksie inaczej jest
# zdjecia_kalibracja = zapisz_n_zdjec(n_zdjec, sciezka_zapisu, "dist_cal", 0)
# zdjecia_kalibracja = ['D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_0.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_1.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_2.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_3.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_4.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_5.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_6.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_7.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_8.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_9.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_10.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_11.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_12.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_13.jpg']
zdjecia_kalibracja = glob.glob(sciezka_zapisu + "dist_cal*.jpg")
# print(zdjecia_kalibracja)
# mtx, dist, new_cam_mtx, roi = wsp_znieksztalcenia(zdjecia_kalibracja, sciezka_zapisu)

# undistort
# zdj = cv2.imread(zdjecia_kalibracja[0])
# print(zdjecia_kalibracja[0])
# dst = cv2.undistort(zdj, mtx, dist, None, new_cam_mtx)

# crop the image
# x, y, w, h = roi
# print(roi)
# dst = dst[y:y+h, x:x+w]
# cv2.imwrite(sciezka_zapisu + 'dist_calibres0.png', dst)

# Wyprostuj obraz


# Ustal wartość progową (threshold value) dla maskowania
# Wybór liczby obiektów kalibracji

n_obiekt = int(input("Liczba obiektow kalibracji: "))
zdj = glob.glob(sciezka_zapisu + "object_*.jpg")
print(zdj)
# zdj = glob.glob(".\\test_img\\pieciokat_test*.jpg")
# Pięciokąty:
# zdj = [".\\test_img\\cal_img\\object_1.jpg", ".\\test_img\\cal_img\\object_3.jpg", ".\\test_img\\cal_img\\object_6.jpg"]
i = 0
thresh_ksztalt_wyniki = []
thresh_kolor_wyniki = [0 for col in range(n_obiekt) for row in range(3)]
print(thresh_kolor_wyniki)

cv2.namedWindow("Kalibracja", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Kalibracja", 668, 500)

# Zmienne do wyswietlania obrazu
# kolor = (255, 0, 0)
# font = cv2.FONT_HERSHEY_DUPLEX

# Wybór kształtu i koloru kolejnego obiektu 
while n_obiekt:
    thresh_ksztalt = 255
    # thresh_kolor_dolny = 
    spr_wybor = 1
    # Wybor ksztaltu
    while(spr_wybor):
        ksztalt = input("Ksztalt podstawy: [p - prostokat, t - trójkat, k - pięciokąt]: ")
        match ksztalt:
            case 'p':
                ksztalt_wybor = 4
                spr_wybor = 0
            case 't':
                ksztalt_wybor = 3
                spr_wybor = 0
            case 'k':
                ksztalt_wybor = 5
                spr_wybor = 0
            case _:
                print("ERROR: Wybierz poprawna opcje!")

    spr_wybor = 1
    # Wybor koloru
    while(spr_wybor):
        kolor = input("Kolor: [r - czerwony, g - zielony, b - niebieski]: ")
        match kolor:
            case 'r':
                kolor_wybor = 1
                spr_wybor = 0
            case 'g':
                kolor_wybor = 2
                spr_wybor = 0
            case 'b':
                kolor_wybor = 3
                spr_wybor = 0
            case _:
                print("ERROR: Wybierz poprawna opcje!")

    # Umieszczenie obiektu przed kamerą i uchwycenie jego zdjęcia
    print("Umieść obiekt przed kamerą i wykonaj zdjęcie")
    # zdj = zapisz_n_zdjec(1, sciezka_zapisu, "obiekt", 1)
    # zdj = glob.glob(sciezka_zapisu + 'obiekt*.jpg')
    # zdj = [".\\test_img\\cal_img\\object_8.jpg"]
    # print(zdj)
    # zdj = "D:\\studia\\inzynierka\\app\\test_img\\cal_img\\obiekt0.jpg"
    # Szukaj kształtu z różnymi wartościami thresh
    # thresh_ksztalt_temp = thresh_ksztalt

    while True:
        thresh_ksztalt -= 1
        if thresh_ksztalt <= 0:
            break

        check, ksztalt, coords, zdj_ksztalt, tekst = detekcja_ksztaltu(zdj[i], thresh_ksztalt)
        print('ksztalt: ' + str(ksztalt))
        print('ksztalt_wybor: ' + str(ksztalt_wybor))
        print('check: ' + str(check))
        print('thresh: ' + str(thresh_ksztalt))

        cv2.imshow("Kalibracja", zdj_ksztalt)
        cv2.waitKey(100)

        if check and (ksztalt == ksztalt_wybor):
            spr = input("Czy widoczny kształt? [t/n]: ")
            match spr:
                case 't':
                    break
                case 'n':
                    thresh_ksztalt -= 5
                    continue
    thresh_ksztalt_wyniki.append(thresh_ksztalt)

    # while ksztalt != ksztalt_wybor and thresh_ksztalt_temp >= 0:
    #     thresh_ksztalt_temp -= 1
    #     check, ksztalt, coords = detekcja_ksztaltu(zdj[i], thresh_ksztalt_temp)
    #     print('ksztalt: ' + str(ksztalt))
    #     print('ksztalt_wybor: ' + str(ksztalt_wybor))
    #     print('check: ' + str(check))
    #     print('thresh: ' + str(thresh_ksztalt_temp))
    # thresh_ksztalt = thresh_ksztalt_temp
    print(thresh_ksztalt_wyniki)

    # Szukaj koloru z różnymi wartościami thresh
    while True:
        thresh_ksztalt -= 1
        if thresh_ksztalt <= 0:
            break

        check, ksztalt, coords, zdj_ksztalt, tekst = detekcja_ksztaltu(zdj[i], thresh_ksztalt)
        print('ksztalt: ' + str(ksztalt))
        print('ksztalt_wybor: ' + str(ksztalt_wybor))
        print('check: ' + str(check))
        print('thresh: ' + str(thresh_ksztalt))

        cv2.imshow("Kalibracja", zdj_ksztalt)
        cv2.waitKey(100)

        if check and (ksztalt == ksztalt_wybor):
            spr = input("Czy widoczny kształt? [t/n]: ")
            match spr:
                case 't':
                    break
                case 'n':
                    thresh_ksztalt -= 5
                    continue
    thresh_ksztalt_wyniki.append(thresh_ksztalt)

    # Zapisz znalezione wartości

    n_obiekt -= 1
    i += 1
    print(n_obiekt)
    print('end of iteration')



# Zapis wartości do listy

# Wyznaczenie wartości progowej
