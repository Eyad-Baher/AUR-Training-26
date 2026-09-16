import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread(r'Phase3\task1\face.jpg')

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

k_size = 5

avg_blur = cv2.blur(gray,(k_size,k_size))
median_blur = cv2.medianBlur(gray,k_size)
gaussian_blur = cv2.GaussianBlur(gray,(k_size, k_size),0)

t_lower, t_upper = 50, 150

edges_avg = cv2.Canny(avg_blur, t_lower, t_upper)
edges_median = cv2.Canny(median_blur, t_lower, t_upper)
edges_gaussian = cv2.Canny(gaussian_blur, t_lower, t_upper)

plt.figure(figsize=(14, 7))

plt.subplot(2, 4, 1)
plt.imshow(gray, cmap='gray')
plt.title('Original Noisy Face')


plt.subplot(2, 4, 2)
plt.imshow(avg_blur, cmap='gray')
plt.title('Average Blur')


plt.subplot(2, 4, 3)
plt.imshow(median_blur, cmap='gray')
plt.title('Median Blur')


plt.subplot(2, 4, 4)
plt.imshow(gaussian_blur, cmap='gray')
plt.title('Gaussian Blur')


plt.subplot(2, 4, 6)
plt.imshow(edges_avg, cmap='gray')
plt.title('Canny (Average)')


plt.subplot(2, 4, 7)
plt.imshow(edges_median, cmap='gray')
plt.title('Canny (Median)')


plt.subplot(2, 4, 8)
plt.imshow(edges_gaussian, cmap='gray')
plt.title('Canny (Gaussian)')


plt.tight_layout()
plt.show()