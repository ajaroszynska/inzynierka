import cv2
import numpy as np

# Single files - in final app version with GUI it should be fragmented
# i.e. file-opening script, detection script, drawing script, coors-sending script

zdj = cv2.imread('app\\test_img\\test1.png')
# zdj = cv2.VideoCapture albo wgl funkcja pobierz_obraz

# konwersja RBG -> HSV
hsv_zdj = cv2.cvtColor(zdj, cv2.COLOR_BGR2HSV)

# !! Zakresy pewnie trzeba będzie dostosowywać z kalibracji kamery

# Zakres i maska dla czerwonego
r_dolny = np.array([136, 87, 11], np.uint8)
r_gorny = np.array([180, 255, 255], np.uint8)
r_maska = cv2.inRange(hsv_zdj, r_dolny, r_gorny)

# Zielony
g_dolny = np.array([25, 52, 72], np.uint8)
g_gorny = np.array([102, 255, 255], np.uint8)
g_maska = cv2.inRange(hsv_zdj, g_dolny, g_gorny)

# Niebieski
b_dolny = np.array([94, 80, 2], np.uint8)
b_gorny = np.array([120, 255, 255], np.uint8)
b_maska = cv2.inRange(hsv_zdj, b_dolny, b_gorny)

# Morphological Transform: Dilation (remove noise)
# bitwise_and między klatką a maską wykrywający 1 kolor

kernel = np.ones((5,5), "uint8")

# czerwony
r_maska = cv2.dilate(r_maska, kernel)
wynik_r = cv2.bitwise_and(zdj, zdj, mask = r_maska)

# zielony
g_maska = cv2.dilate(g_maska, kernel)
wynik_g = cv2.bitwise_and(zdj, zdj, mask = g_maska)

# zielony
b_maska = cv2.dilate(b_maska, kernel)
wynik_b = cv2.bitwise_and(zdj, zdj, mask = b_maska)


r_pola = []
g_pola = []
b_pola = []

# czerwony

# kontury

r_kontury, r_hierarchia = cv2.findContours(r_maska, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
g_kontury, g_hierarchia = cv2.findContours(g_maska, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
b_kontury, b_hierarchia = cv2.findContours(b_maska, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

kontury = [r_kontury,
           g_kontury, 
           b_kontury]

hierarchia = [r_hierarchia, 
              g_hierarchia, 
              b_hierarchia]
# koordynaty znalezionych obiektów



# Iterating through each contour to retrieve coordinates of each shape
for i, kontur in enumerate(kontury[0]):
    # Calculate the area of the detected shape
    area = cv2.contourArea(kontur)
    r_pola.append(area)
    # # print("area[{}]= {}".format(i,areas[i]))
    # if (area > 300):    # tutaj chyba też z kalibracji
    #     x, y, w, h = cv2.boundingRect(kontur) 
    #     zdj = cv2.rectangle(zdj, (x, y), (x + w, y + h), (0, 0, 255), 2)
    #     # Setting some variables which will be used to display text on the final image
    #     coords = (x, y)
    #     print("coords = {}".format(coords))
    #     kolor = (0, 0, 255)
    #     font = cv2.FONT_HERSHEY_DUPLEX
    #     cv2.putText(zdj, "Czerwony", coords, font, 1.0, kolor)


# zielony

# kontury


# Iterating through each contour to retrieve coordinates of each shape
for i, kontur in enumerate(kontury[1]):
    # Calculate the area of the detected shape
    area = cv2.contourArea(kontur)
    g_pola.append(area)
    # # print("area[{}]= {}".format(i,areas[i]))
    # if (area > 300):
    #     x, y, w, h = cv2.boundingRect(kontur) 
    #     zdj = cv2.rectangle(zdj, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #     # Setting some variables which will be used to display text on the final image
    #     coords = (x, y)
    #     print("coords = {}".format(coords))
    #     kolor = (0, 255, 0)
    #     font = cv2.FONT_HERSHEY_DUPLEX
    #     cv2.putText(zdj, "Zielony", coords, font, 1.0, kolor)

# niebieski

# kontury


# Iterating through each contour to retrieve coordinates of each shape
for i, kontur in enumerate(kontury[2]):
    # Calculate the area of the detected shape
    area = cv2.contourArea(kontur)
    b_pola.append(area)
    # # print("area[{}]= {}".format(i,areas[i]))
    # if (area > 300):
    #     x, y, w, h = cv2.boundingRect(kontur) 
    #     zdj = cv2.rectangle(zdj, (x, y), (x + w, y + h), (255, 0, 0), 2)
    #     # Setting some variables which will be used to display text on the final image
    #     coords = (x, y)
    #     print("coords = {}".format(coords))
    #     kolor = (255, 0, 0)
    #     font = cv2.FONT_HERSHEY_DUPLEX
    #     cv2.putText(zdj, "Niebieski", coords, font, 1.0, kolor)


# The biggest shape is our object

# Wyrównanie długości list
max_dlugosc = max(len(r_pola), len(g_pola), len(b_pola))

while(max_dlugosc > len(r_pola)):
    r_pola.append(0)

while(max_dlugosc > len(g_pola)):
    g_pola.append(0)

while(max_dlugosc > len(b_pola)):
    b_pola.append(0)

pola = np.array([r_pola,
        g_pola, 
        b_pola])
print(pola)

obj_pole = np.max(pola)
obj_index = np.where(pola==obj_pole)

print("Biggest shape has the area of pola{},{} = {}".format(obj_index[0],obj_index[1], obj_pole))

obj_kontur = kontury[obj_index[0].item()][obj_index[1].item()]
print(obj_kontur)

match obj_index[0].item():
    case 0:
        kolor = (0, 0, 255)
        tekst = "Czerwony"
    case 1:
        kolor = (0, 255, 0)
        tekst = "Zielony"
    case 2:
        kolor = (255, 0, 0)
        tekst = "Niebieski"
    case _:
        print("Too many rows in the color matrix")

x, y, w, h = cv2.boundingRect(obj_kontur) 
zdj = cv2.rectangle(zdj, (x, y), (x + w, y + h), kolor, 2)
# Setting some variables which will be used to display text on the final image
coords = (x, y)
print("coords = {}".format(coords))

font = cv2.FONT_HERSHEY_DUPLEX
cv2.putText(zdj, tekst, coords, font, 1.0, kolor)
        
# obj_contour = contours[obj_index]

# epsilon = 0.01 * cv2.arcLength(obj_contour, True)
# approx = cv2.approxPolyDP(obj_contour, epsilon, True)
# cv2.drawContours(image, obj_contour, -1, (255, 0, 0), 8)


# # Retrieving coordinates of the contour so that we can put text over the shape
# x, y, w, h = cv2.boundingRect(approx)
# x_mid = int(x + (w/3)) # estimation - middle of the shape on the X axis
# y_mid = int(y + (h/1.5)) # estimation - middle of the shape on the Y axis
# # Setting some variables which will be used to display text on the final image
# coords = (x_mid, y_mid)
# print("coords = {}".format(coords))
# colour = (0, 0, 0)
# font = cv2.FONT_HERSHEY_DUPLEX



# Display the image with detected shape
cv2.imshow("shapes_detected", zdj)
cv2.waitKey(0)