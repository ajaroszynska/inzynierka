import cv2
from pathlib import Path



def zapisz_n_zdjec(n_zdjec, sciezka_zapisu, nazwa_pliku, opcja_dialog=1):
    # Stworz folder na zdjęcia jeśli nie istnieje, jak istnieje to ignoruj
    Path(sciezka_zapisu).mkdir(exist_ok = True)

    zdjecia = []

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
            print("Nie można otworzyć kamery")
            return

    zdj_licznik = 0

    match opcja_dialog:
         case 0:
              opcja = 'szachownicę'
         case 1:
              opcja = 'obiekt'
         case _:
              opcja = 'obiekt'

    print("Wykonaj min {} zdjec".format(n_zdjec))
    print('Umieść {} w kadrze i naciśnij "c" aby zrobic zdjecie'.format(opcja))
    print('Nacisnij "q" aby zakonczyc robienie zdjec')

    while n_zdjec:
        ok, zdj = cam.read()
        if not ok:
            print("Błąd odczytu klatki")
            break
        
        r = cv2.resize(zdj, (267, 200))
        cv2.imshow('podglad', r)
        # print('Ilosc wykonanych do tej pory zdjec: {}'.format(img_count))
        k = cv2.waitKey(1)

        if k == ord('q'):
            print('Nacisnieto "q", konczenie wykonywania zdjec...')
            break
        elif k == ord('c'):
            zdj_nazwa = sciezka_zapisu + nazwa_pliku + "{}.jpg".format(zdj_licznik)
            cv2.imwrite(zdj_nazwa, zdj)
            print("Zapisano {}".format(zdj_nazwa))
            zdjecia.append(zdj_nazwa)
            zdj_licznik += 1
            n_zdjec -= 1
            print("Pozostało zdjęć do zrobienia: {}".format(n_zdjec))

    cam.release()
    cv2.destroyAllWindows()
    return zdjecia
