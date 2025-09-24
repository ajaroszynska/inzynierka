import cv2

c = cv2.VideoCapture(0)

while(True):
    _, frame = c.read()
    mirror = cv2.flip(frame, 1)
    r = cv2.resize(mirror, (600, 400))
    
    cv2.imshow('okienko', r)
    
    if cv2.waitKey(1)==ord("q"):
        break
    
c.release()
cv2.destroyAllWindows()