import cv2

def detekcja_ksztaltu(zdj_sciezka, thresh ):
    # Pobranie zdjęcia i konwersja na skalę szarości
    zdj = cv2.imread(zdj_sciezka)
    gray = cv2.cvtColor(zdj, cv2.COLOR_BGR2GRAY)

    # Konwersja do obrazu czarno białego bez skali szarości
    _, zdj_thresh = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
    cv2.imshow("zdj thresh", zdj_thresh)
    cv2.waitKey(100)

    # Szukanie konturów i detekcja największego kształtu
    kontury, hierarchia = cv2.findContours(zdj_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    pola = []
    for i, k in enumerate(kontury):
        # Pole powierzchni konturu
        pola.append(cv2.contourArea(k))
    
    obj_pole = max(pola)
    obj_index = pola.index(obj_pole)
    print("Najwiekszy ksztalt ma obszar: pola[{}] = {}".format(obj_index, obj_pole))

    # Przyblizenie ksztaltu aby wyeliminować szumy i niedokładności
    obj_kontur = kontury[obj_index]

    eps = 0.01 * cv2.arcLength(obj_kontur, True)
    approx = cv2.approxPolyDP(obj_kontur, eps, True)
    cv2.drawContours(zdj, obj_kontur, -1, (255,0,0), 8)

    # Wyznacz wspołrzędne obiektu
    x, y, w, h = cv2.boundingRect(approx)
    x_mid = int(x + (w/3))
    y_mid = int(y + (h/1.5))
    coords = (x_mid, y_mid)

    # Zmienne do wyswietlania obrazu
    kolor = (0, 0, 0)
    font = cv2.FONT_HERSHEY_DUPLEX

    if len(approx) == 3:
        # Trójkąt
        ksztalt = 3
        check = True
        cv2.putText(zdj, "Trójkąt", coords, font, 1, kolor, 1)
    elif len(approx) == 4:
        # Prostokąt
        ksztalt = 4
        check = True
        cv2.putText(zdj, "Prostokąt", coords, font, 1, kolor, 1)

    elif len(approx) == 5:
        # Pięciokąt
        ksztalt = 5
        check = True
        cv2.putText(zdj, "Pięciokąt", coords, font, 1, kolor, 1)
    else:
        # Brak
        ksztalt = 0
        check = False
        cv2.putText(zdj, "Brak", coords, font, 1, kolor, 1)

    return check, ksztalt, coords