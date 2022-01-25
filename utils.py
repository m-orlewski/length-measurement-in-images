import cv2
import imutils
from imutils import perspective
import numpy as np
from scipy.spatial import distance


def labelObjects(img):
   
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edges = cv2.erode(edged, None, iterations=1)

    contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    objects = 0

    for c in contours:
        if cv2.contourArea(c) < 70:
            continue
        objects += 1
        M= cv2.moments(c)
        cx= int(M['m10']/M['m00']) - 10
        cy= int(M['m01']/M['m00']) + 10
        cv2.putText(img, text= str(objects), org=(cx,cy),
                fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5, color=(0,255,0),
                thickness=2, lineType=cv2.LINE_AA)

    return img, objects, edges

def measureObjects(edges, choice, width, img):
    contours = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    contours = list(contours)
    for i, contour in enumerate(contours):
        if cv2.contourArea(contour) < 70:
            contours.remove(contour)
            

    pixels_per_metric = calculatePixelsPerMetric(contours[int(choice)-1], width)

    for contour in contours:
        box = cv2.minAreaRect(contour)
        if imutils.is_cv2():
            box = cv2.cv.BoxPoints(box)
        else:
            box = cv2.boxPoints(box)
            
        box = np.array(box, dtype='int')
        box = perspective.order_points(box)

    

        (tl, tr, br, bl) = box
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)

        dA = distance.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB = distance.euclidean((tlblX, tlblY), (trbrX, trbrY))

        dimA = dA / pixels_per_metric
        dimB = dB / pixels_per_metric

        cv2.putText(img, "{:.3f}cm".format(dimA),
		(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (255, 255, 255), 2)
        cv2.putText(img, "{:.3f}cm".format(dimB),
		(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (255, 255, 255), 2)

        cv2.drawContours(img, [box.astype('int')], -1, (255, 0, 0), 2)

    return img

def calculatePixelsPerMetric(contours, width):
        box = cv2.minAreaRect(contours)
        
        if imutils.is_cv2():
            box = cv2.cv.BoxPoints(box)
        else:
            box = cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        box = imutils.perspective.order_points(box)

        (tl, tr, br, bl) = box
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)
        dB = distance.euclidean((tlblX, tlblY), (trbrX, trbrY))

        return dB/width
        
def midpoint(A, B):
	return ((A[0] + B[0]) * 0.5, (A[1] + B[1]) * 0.5)