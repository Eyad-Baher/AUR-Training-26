import cv2
import numpy as np


global height,width
height = 1000
width = 700

def draw_windows(ids,img):
    count = 0
    for i in range(6):
        for j in range(5):

            y0 = int(height*0.1)+i*100+20
            y1 = int(height*0.1)+i*100 +70
            x0 = int(width*0.2)+j*75 +15
            x1 = int(width*0.2)+j*75 +45

            # img[yo:y1,x0:x1] = (255,220,120)
            # img[yo:y1,x0:x1] = (20,20,30)

            light = light_windows(ids,count)

            if light:
                img[y0:y1,x0:x1] = (255,220,120)
            else:
                img[y0:y1,x0:x1] = (20,20,30)

            count+=1

    return img

def light_windows(ids,id):
    return id in ids

img = np.zeros((height,width,3),dtype=np.uint8)

img[:,:] = (25,25,40)

img[int(0.75 * height):,:] = (30,50,35)

img[int(0.1*height):int(0.8 * height),int(0.2*width):int(0.7*width)] = (90,90,100)


while True:
    window_ids = []
    window_ids = np.random.choice(30,4,replace=False)
    
    img = draw_windows(window_ids,img)

    cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

    cv2.imshow("landscape image",img)
    if cv2.waitKey(1000) == 27:
        break
cv2.destroyAllWindows()

