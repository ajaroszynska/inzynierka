import cv2
from zapisz_n_zdjec import *
from wsp_znieksztalcenia import *
from detekcja_ksztaltu import *

# Skrypt kalibracji kamery

# Wyznacz współczynniki zniekształcenia i macierz kamery
# Zrób min. 10 zdjęć z szachownicą w różnych pozycjach
# Szachownica musi być asymetryczna, np. 8x5; 5x5 nie zadziała!
# n_zdjec = int(input("Podaj liczbe zdjec do wyznaczenia wsp znieksztalcenia (min. 10): "))
sciezka_zapisu = "D:\\studia\\inzynierka\\app\\test_img\\cal_img\\" # placeholder - w linuksie inaczej jest
# zdjecia_kalibracja = zapisz_n_zdjec(n_zdjec, sciezka_zapisu, "dist_cal", 0)
zdjecia_kalibracja = ['D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_0.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_1.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_2.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_3.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_4.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_5.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_6.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_7.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_8.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_9.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_10.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_11.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_12.jpg', 'D:\\studia\\inzynierka\\app\\test_img\\cal_img\\cal_test_13.jpg']

wsp_znieksztalcenia(zdjecia_kalibracja, sciezka_zapisu)

# Wyprostuj obraz


# Ustal wartość progową (threshold value) dla maskowania
# Wybór liczby obiektów kalibracji
thresh_ksztalt = 0

n_obiekt = int(input("Liczba obiektow kalibracji: "))

# Wybór kształtu i koloru kolejnego obiektu 
while n_obiekt:
    spr_wybor = 1
    # Wybor ksztaltu
    while(spr_wybor):
        ksztalt = input("Ksztalt podstawy: [p - prostokat, t - trójkat, k - kolo]: ")
        match ksztalt:
            case 'p':
                ksztalt_wybor = 0
                spr_wybor = 0
            case 't':
                ksztalt_wybor = 1
                spr_wybor = 0
            case 'k':
                ksztalt_wybor = 2
                spr_wybor = 0
            case _:
                print("ERROR: Wybierz poprawna opcje!")

    spr_wybor = 1
    # Wybor koloru
    while(spr_wybor):
        kolor = input("Kolor: [r - czerwony, g - zielony, b - niebieski]: ")
        match kolor:
            case 'r':
                kolor_wybor = 0
                spr_wybor = 0
            case 'g':
                kolor_wybor = 1
                spr_wybor = 0
            case 'b':
                kolor_wybor = 2
                spr_wybor = 0
            case _:
                print("ERROR: Wybierz poprawna opcje!")

    # Umieszczenie obiektu przed kamerą i uchwycenie jego zdjęcia
    print("Umieść obiekt przed kamerą i wykonaj zdjęcie")
    zdj = zapisz_n_zdjec(1,"D:\\studia\\inzynierka\\app\\test_img\\cal_img\\", "obiekt", 1)
    print(zdj)
    # zdj = "D:\\studia\\inzynierka\\app\\test_img\\cal_img\\obiekt0.jpg"
    # Szukaj kształtu z różnymi wartościami thresh
    thresh_ksztalt_temp = thresh_ksztalt

    check, ksztalt, coords = detekcja_ksztaltu(zdj[0], thresh_ksztalt_temp)

    while (not check and ksztalt != ksztalt_wybor) or thresh_ksztalt_temp <= 255:
        thresh_ksztalt_temp += 1
        check, ksztalt, coords = detekcja_ksztaltu(zdj[0], thresh_ksztalt_temp)
    
    thresh_ksztalt = thresh_ksztalt_temp
    print(thresh_ksztalt)
    # Szukaj koloru z różnymi wartościami thresh


    # Zapisz znalezione wartości

    n_obiekt -= 1
    print(n_obiekt)
    print('end of iteration')



# Zapis wartości do listy

# Wyznaczenie wartości progowej
