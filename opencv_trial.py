import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def draw_rect(frame):

    # Draw five boxes for fingers

    global x_box, y_box, num_of_rect

    num_of_rect = 5
    x_box = [50, 110, 175, 240, 290]
    y_box = [100, 80,60, 80, 190]

    for i in range(num_of_rect):
        cv2.rectangle(roi, (x_box[i], y_box[i]), (x_box[i] + 20,  y_box[i] + 20), (255, 0, 0), 2)

    return frame

def get_hsv(frame):

    global min_skin, max_skin

    min_skin = max_skin = cv2.sumElems(frame[x_box[0] + 20: y_box[0] + 20])

    for i in range(num_of_rect):
        roi = frame[x_box[i] + 20: y_box[i] + 20]
        roi = cv2.cvtColor(cv2.COLOR_BGR2HSV)
        
        if cv2.sumElems(roi) < min_skin:
            min_skin = roi
        if cv2.sumElems(roi) > max_skin:
            max_skin = roi

    return

while True:
    ret, frame = cap.read()

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, 'Region Of Interest', (0, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.rectangle(frame, (15,90), (300, 380), (0,255,0), 5)

    roi = frame[90:380, 15:300]
    roi = cv2.resize(roi, (400,400))

    roi = draw_rect(roi)

    if cv2.waitKey(1) & 0xFF == ord("t"):
        get_hsv(roi)

    #cvt_to_HSV = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    #skin_mask = cv2.inRange(cvt_to_HSV, min_skin, max_skin)

    #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))

    #skin_mask = cv2.erode(skin_mask, kernel, iterations = 2)
    #skin_mask = cv2.dilate(skin_mask, kernel, iterations = 2)

    #skin_mask = cv2.GaussianBlur(skin_mask, (3, 3), 0)
    #skin = cv2.bitwise_and(roi, roi, mask = skin_mask)

    cv2.imshow("frame", frame)
    cv2.imshow("roi", roi)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
