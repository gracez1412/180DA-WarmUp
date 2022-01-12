import numpy as np 
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # capture frame-by-frame
    ret, frame = cap.read()

    # our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # do basic template matching to "detect" object
    template = cv2.imread('C:/users/lolly/OneDrive/Documents/UCLA Textbooks/180DA-WarmUp/Images/object-template.png',0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(gray,template,cv2.TM_CCOEFF_NORMED)
    min_val, max_loc, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(gray, top_left, bottom_right, 255, 2)
    # print(str(top_left[0]) + ', ' + str(top_left[1]))
    coord_str = '(' + str(top_left[0]) + ', ' + str(top_left[1]) + ')'
    cv2.putText(gray, coord_str, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2)

    # display the resulting frame
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()