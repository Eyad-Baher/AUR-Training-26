import cv2
import numpy as np

class ShapeDetector:

    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(video_path)

        self.lower_red1 = np.array([0, 50, 50])
        self.upper_red1 = np.array([10, 255, 255])
        self.lower_red2 = np.array([170, 50, 50])
        self.upper_red2 = np.array([179, 255, 255])

        self.lower_blue = np.array([100, 50, 50])
        self.upper_blue = np.array([140, 255, 255])

    def process_mask(self, mask, color_name, frame): 
    
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
            
                cv2.drawContours(frame, [c], -1,[255,255,255] , 2)
                cv2.putText(frame, shape, (cx - 40, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, [245, 230, 175], 2)

    def run(self):
        if not self.cap.isOpened():
            print("Error: Could not open video.")
            return

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            blur = cv2.GaussianBlur(frame, (5, 5), 0)
            hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

            mask_red1 = cv2.inRange(hsv, self.lower_red1, self.upper_red1)
            mask_red2 = cv2.inRange(hsv, self.lower_red2, self.upper_red2)

            mask_red = mask_red1 | mask_red2
            mask_blue = cv2.inRange(hsv, self.lower_blue, self.upper_blue)

            self.process_mask(mask_red, "Red", frame)
            self.process_mask(mask_blue, "Blue", frame)

            cv2.imshow('Subtask 2 - Shape Detector', frame)

            if cv2.waitKey(80) == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    detector = ShapeDetector("thrown_shapes_noisy_30s.mp4")
    detector.run()