import cv2

def detekcja_ksztaltu(zdj_sciezka, thresh ):
    # Pobranie zdjęcia i konwersja na skalę szarości
    zdj = cv2.imread(zdj_sciezka)
    gray = cv2.cvtColor(zdj, cv2.COLOR_BGR2GRAY)

    # Konwersja do obrazu czarno białego bez skali szarości
    _, zdj_thresh = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY_INV)
    # resize = cv2.resize(zdj_thresh, (267, 200))
    # cv2.imshow("zdj thresh", resize)
    # cv2.waitKey(100)

    # Szukanie konturów i detekcja największego kształtu
    kontury, hierarchia = cv2.findContours(zdj_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    pola = []
    for i, k in enumerate(kontury):
        # Pole powierzchni konturu
        pola.append(cv2.contourArea(k))
    try:
        obj_pole = max(pola)
        obj_index = pola.index(obj_pole)
    except:
        print("No objects found")
        check = False
        ksztalt = 0
        coords = 0
        tekst = "brak"
        return check, ksztalt, coords, zdj_thresh, tekst
    
    print("Najwiekszy ksztalt ma obszar: pola[{}] = {}".format(obj_index, obj_pole))

    # Przyblizenie ksztaltu aby wyeliminować szumy i niedokładności
    obj_kontur = kontury[obj_index]

    eps = 0.05 * cv2.arcLength(obj_kontur, True)
    approx = cv2.approxPolyDP(obj_kontur, eps, True)
    # cv2.drawContours(zdj_thresh, obj_kontur, -1, (255,0,0), 8)

    # r = cv2.resize(zdj_thresh, (267,200))
    # cv2.imshow('test', r)
    # cv2.waitKey(500)

    # Wyznacz wspołrzędne obiektu
    x, y, w, h = cv2.boundingRect(approx)
    x_mid = int(x + (w/3))
    y_mid = int(y + (h/1.5))
    coords = (x_mid, y_mid)


    if len(approx) == 3:
        # Trójkąt
        ksztalt = 3
        check = True
        tekst = "Trojkat"
    elif len(approx) == 4:
        # Prostokąt
        ksztalt = 4
        check = True
        tekst = "Prostokat"
    elif len(approx) == 5:
        # Pięciokąt
        ksztalt = 5
        check = True
        tekst = 'Pieciokat'
    else:
        # Brak
        ksztalt = 0
        check = False
        tekst = "Brak"
    
    cv2.imwrite(".\\test_img\\cal_img\\" + "temp.png", zdj_thresh)
    zdj_wynik = cv2.imread(".\\test_img\\cal_img\\" + "temp.png")
    kolor = (0, 255, 0)
    font = cv2.FONT_HERSHEY_DUPLEX
    zdj_wynik = cv2.rectangle(zdj_wynik, (x, y), (x + w, y + h), kolor, 3)
    cv2.putText(zdj_wynik, tekst, coords, font, 1, kolor, 1)

    return check, ksztalt, coords, zdj_wynik, tekst