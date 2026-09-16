import cv2

image = cv2.imread(r"Phase3\workshop1\task3.jpg")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

blurred = cv2.GaussianBlur(gray, (5, 5), 0)

_, thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY_INV)

contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

img_height, img_width = image.shape[:2]
image_area = img_height * img_width

for c in contours:
    area = cv2.contourArea(c)
    
    if area < 500 or area > (image_area * 0.8):
        continue

    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.03 * peri, True) 
    vertices = len(approx)

    if vertices == 3:
        shape = "Triangle"
    elif vertices == 4:
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = float(w) / h
        shape = "Square" if 0.9 <= aspect_ratio <= 1.1 else "Rectangle"
    else:
        shape = "Circle"

    M = cv2.moments(c)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        cv2.putText(image, shape, (cx - 30, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

cv2.imshow('Detected Shapes', image)
cv2.waitKey(0)
cv2.destroyAllWindows()