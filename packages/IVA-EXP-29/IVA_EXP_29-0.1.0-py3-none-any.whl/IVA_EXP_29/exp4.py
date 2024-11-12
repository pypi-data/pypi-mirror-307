def run():
    print(""" EXP 4 YOLO
git clone https://github.com/WongKinYiu/yolov9.git 
!wget  https://github.com/WongKinYiu/yolov9/releases/download/v0.1/yolov9-c-converted.pt 
import matplotlib.pyplot as plt
import cv2
img = cv2.imread('/content/yolov9/data/images/horses.jpg')
plt.figure(figsize=(20,30))     #Sets the size of the figure for displaying the image.
plt.imshow(img)
plt.xticks([])   #Hides the x and y axis ticks for a cleaner look.
#plt.yticks([])
plt.show()
!python /content/yolov9/detect.py --source '/content/yolov9/data/images/horses.jpg' --img 640 \
  --device cpu --weights './yolov9-c-converted.pt' \
  --name yolov9_c_c_640_detect
the detect.py path should be given without paranthesis
img = cv2.imread('/content/yolov9/runs/detect/yolov9_c_c_640_detect6/images.jpeg')
print(img)
plt.figure(figsize=(20,30))
plt.imshow(img)
plt.xticks([])
plt.yticks([])
plt.show()
 """)