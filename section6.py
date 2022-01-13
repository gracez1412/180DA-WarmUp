# https://ckyrkou.medium.com/color-thresholding-in-opencv-91049607b06d

import cv2
cap = cv2.VideoCapture(0)

# in rgb
lower_color_bounds = (30, 20, 20)
upper_color_bounds = (120, 60, 60)

# rgba(83,38,38,255)
# rgba(78,36,41,255)
# rgba(34,28,25,255)
# rgba(34,27,27,255)
# rgba(101,46,50,255)
# rgba(113,52,55,255)

while(True):
    # capture frame-by-frame
    ret, frame = cap.read()

    # our operations on the frame come here
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mask = cv2.inRange(image, lower_color_bounds, upper_color_bounds)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if(w > 20 & h > 10):
            cv2.rectangle(mask, (x,y), (x+w,y+h),(255,255,255),2)

    mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    image = mask_rgb & image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # display the resulting frame
    cv2.imshow('frame', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()