import cv2
import matplotlib.pyplot as plt

def labelObjects(img):
   
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edges = cv2.erode(edged, None, iterations=1)

    contours = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for (i,c) in enumerate(contours):
        if cv2.contourArea(c) < 100:
            continue
        M= cv2.moments(c)
        cx= int(M['m10']/M['m00']) - 10
        cy= int(M['m01']/M['m00']) + 10
        cv2.putText(img, text= str(i+1), org=(cx,cy),
                fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5, color=(0,0,0),
                thickness=2, lineType=cv2.LINE_AA)

           
if __name__ == '__main__':
    labelObjects(1)