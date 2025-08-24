import cv2

# Single files - in final app version with GUI it should be fragmented
# i.e. file-opening script, detection script, drawing script, coors-sending script

# https://www.geeksforgeeks.org/python/multiple-color-detection-in-real-time-using-python-opencv
import numpy as np
import cv2

frame = cv2.imread('app\\test_img\\test1.png')

# RBG -> HSV
hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# !! Zakresy pewnie trzeba będzie dostosowywać z kalibracji kamery

# Zakres i maska dla czerwonego
red_lower = np.array([136, 87, 11], np.uint8)
red_upper = np.array([180, 255, 255], np.uint8)
red_mask = cv2.inRange(hsv_frame, red_lower, red_upper)

# Zielony
green_lower = np.array([25, 52, 72], np.uint8)
green_upper = np.array([102, 255, 255], np.uint8)
green_mask = cv2.inRange(hsv_frame, green_lower, green_upper)

# Niebieski
blue_lower = np.array([94, 80, 2], np.uint8)
blue_upper = np.array([120, 255, 255], np.uint8)
blue_mask = cv2.inRange(hsv_frame, blue_lower, blue_upper)

# Morphological Transform: Dilation (remove noise)
# bitwise_and między klatką a maską wykrywający 1 kolor

kernel = np.ones((5,5), "uint8")

# czerwony
red_mask = cv2.dilate(red_mask, kernel)
res_red = cv2.bitwise_and(frame, frame, mask = red_mask)

# zielony
green_mask = cv2.dilate(green_mask, kernel)
res_green = cv2.bitwise_and(frame, frame, mask = green_mask)

# zielony
blue_mask = cv2.dilate(blue_mask, kernel)
res_blue = cv2.bitwise_and(frame, frame, mask = blue_mask)


# czerwony

# kontury
contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


# koordynaty znalezionych obiektów



# Iterating through each contour to retrieve coordinates of each shape
for i, contour in enumerate(contours):
    # Calculate the area of the detected shape
    area = cv2.contourArea(contour)
    # print("area[{}]= {}".format(i,areas[i]))
    if (area > 300):
        x, y, w, h = cv2.boundingRect(contour) 
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # Setting some variables which will be used to display text on the final image
        coords = (x, y)
        print("coords = {}".format(coords))
        colour = (0, 0, 255)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, "Czerwony", coords, font, 1.0, colour)


# zielony

# kontury
contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Iterating through each contour to retrieve coordinates of each shape
for i, contour in enumerate(contours):
    # Calculate the area of the detected shape
    area = cv2.contourArea(contour)
    # print("area[{}]= {}".format(i,areas[i]))
    if (area > 300):
        x, y, w, h = cv2.boundingRect(contour) 
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Setting some variables which will be used to display text on the final image
        coords = (x, y)
        print("coords = {}".format(coords))
        colour = (0, 255, 0)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, "Zielony", coords, font, 1.0, colour)

# niebieski

# kontury
contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Iterating through each contour to retrieve coordinates of each shape
for i, contour in enumerate(contours):
    # Calculate the area of the detected shape
    area = cv2.contourArea(contour)
    # print("area[{}]= {}".format(i,areas[i]))
    if (area > 300):
        x, y, w, h = cv2.boundingRect(contour) 
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # Setting some variables which will be used to display text on the final image
        coords = (x, y)
        print("coords = {}".format(coords))
        colour = (255, 0, 0)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, "Niebieski", coords, font, 1.0, colour)


# Display the image with detected shape
cv2.imshow("shapes_detected", frame)
cv2.waitKey(0)