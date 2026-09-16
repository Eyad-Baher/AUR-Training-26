
import cv2
import numpy as np
def process_mask(mask, color_name, frame):
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv2.contourArea(c) < 500:
            continue

        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.03 * peri, True)
        vertices = len(approx)

        if color_name == "Red" and vertices > 6:
            shape = 'Red Circle'
        elif color_name == "Blue" and vertices == 4:
            shape = 'Blue Square'
        else:
            continue 

        M = cv2.moments(c)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        
            cv2.drawContours(frame, [c], -1,[255,255,255], 2)
            cv2.putText(frame, shape, (cx - 40, cy), cv2.FONT_HERSHEY_SIMPLEX,  1, [245, 230, 175],2)



cap = cv2.VideoCapture(r'sesesion1\task1\thrown_shapes_noisy_30s.mp4')

if not cap.isOpened():
    print('Camera not open')
    exit()


while True:
    ret, frame = cap.read()

    if not ret:
        print('Can\'t recieve video frames')
        break

    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    blur = cv2.GaussianBlur(hsv,(5,5),0)

    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([179, 255, 255])

    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([140, 255, 255])

    mask_red1 = cv2.inRange(blur,lower_red1,upper_red1)
    mask_red2 = cv2.inRange(blur,lower_red2,upper_red2)
    mask_red = mask_red2 | mask_red1

    mask_blue = cv2.inRange(blur,lower_blue,upper_blue)

    process_mask(mask_red, "Red",  frame)
    process_mask(mask_blue, "Blue",  frame)

    cv2.imshow('Subtask 2 - Shape Detection', frame)

    if cv2.waitKey(100) == 27:
        break

cap.release()
cv2.destroyAllWindows()

