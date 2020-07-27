import cv2
import numpy as np
import pickle
import math
import pyautogui as pyauto

cap = cv2.VideoCapture(0)

min_skin = pickle.load(open(r"C:\Users\chuen\Desktop\Python\max_hsv_skin.pickle", "rb"))
max_skin = pickle.load(open(r"C:\Users\chuen\Desktop\Python\min_hsv_skin.pickle", "rb"))

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

    #print(frame[x_box[0] : x_box[0] + 20, y_box[0] : y_box[0] + 20])

    min_skin = [255, 255, 255]
    max_skin = [0, 0, 0]

    #print(min_skin)
    #print(max_skin)

    print(frame[y_box[0] : y_box[0] + 20, x_box[0] : x_box[0] + 20])
    print(frame[y_box[0] : y_box[0] + 20, x_box[0] : x_box[0] + 20][0])

    for i in range(1, num_of_rect):
        roi = frame[y_box[0] : y_box[0] + 20, x_box[0] : x_box[0] + 20]
        for line in roi:
            for pixel in line:
                for i in range(3):
                    if pixel[i] > max_skin[i]:
                        max_skin[i] = pixel[i]

                    if pixel[i] < min_skin[i]:
                        min_skin[i] = pixel[i]
    print(min_skin)
    print(max_skin)
    return

def find_centroid(contour):

    moment = cv2.moments(contour)
    cx = int(moment['m10'] / moment['m00'])
    cy = int(moment['m01'] / moment['m00'])
    return cx, cy

def find_farthest(cx, cy, hull_points):

    hull_points = hull_points[0]

    furth_x = hull_points[0][0]
    furth_y = hull_points[0][1]

    max_dist = math.sqrt(pow(cx - furth_x, 2) + pow(cy - furth_y, 2))

    for x, y in hull_points:
        if math.sqrt(pow(cx - x, 2) + pow(cy - y, 2)) > max_dist:
            furth_x = x
            furth_y = y

    return furth_x, furth_y, max_dist

count = 0

while True:

    ret, frame = cap.read()

    # Defines the region of interest for our hand
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, 'Region Of Interest', (0, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.rectangle(frame, (15,90), (300, 380), (0,255,0), 5)
    roi = frame[90:380, 15:300]

    # Converts Image to Grayscale
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Uses GaussianBlur to remove noise from image
    blur_roi = cv2.GaussianBlur(roi, (5,5), 0)

    blur_roi = cv2.erode(blur_roi, None, iterations = 2)
    blur_roi = cv2.dilate(blur_roi, None, iterations = 2)

    # HSv range for detecting skin (note can vary depending on person)
    min_skin = np.array([0, 58, 30], dtype = "uint8")
    max_skin = np.array([33, 255, 255], dtype = "uint8")

    # Converts our image to HSV (Hue Saturation Value)
    roi_HSV = cv2.cvtColor(blur_roi, cv2.COLOR_BGR2HSV)

    skin_mask = cv2.inRange(roi_HSV, min_skin, max_skin) # Been reversed

    contours, val1 = cv2.findContours(skin_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    max_contour = max(contours, key = cv2.contourArea)
    return_hull = cv2.convexHull(max_contour)
    hull = [cv2.convexHull(contour) for contour in contours]

    cx, cy = find_centroid(max_contour)
    cv2.circle(roi, (cx, cy), 5, [255, 255, 0], -1)


    dx, dy, max_dist = find_farthest(cx, cy, return_hull)

    if count and dx < old_dx + 2.5 and dx > old_dx - 2.5:
        dx = old_dx

    if count and dy < old_dy + 2.5 and dy > old_dy - 2.5:
        dy = old_dy

    cv2.circle(roi , (dx, dy) , 5, [0,0,255], -1 )

    print(max_dist)
    pyauto.moveTo(dx * 6.736, dy * 5.684)

    old_dx = dx
    old_dy = dy

    count += 1

    """for contour in contours:
        area = cv2.contourArea(contour)
        if area > 5000:
            cv2.drawContours(roi, hull, -1, (0, 255, 0), 3)"""

    #for i in range(defects.shape[0]):
        #s, e, f, d = defects[i, 0]
        #furthest = tuple(contour[f][0])

        #cv2.circle(roi, furthest, 5, [0, 0, 255], -1)

    cv2.imshow("frame", frame)
    cv2.imshow("roi", roi)

    cv2.imshow("skin", skin_mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
