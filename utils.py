import cv2
import imutils
from imutils import perspective
import numpy as np
from scipy.spatial import distance


def labelObjects(img):
    '''Oznacza obiekty na obrazie i numeruje je'''

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edges = cv2.erode(edged, None, iterations=1)

    #kontury obiektów
    contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    objects = 0

    #odrzucenie obiektów o małej powierzchni i ponumerowanie pozostałych
    for c in contours:
        if cv2.contourArea(c) < 70:
            continue
        objects += 1
        M = cv2.moments(c)
        cx = int(M['m10']/M['m00']) - 10
        cy = int(M['m01']/M['m00']) + 10
        cv2.putText(img, text= str(objects), org=(cx,cy), fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5, color=(0,255,0), thickness=3, lineType=cv2.LINE_AA)

    return img, objects, edges

def measureObjects(edges, choice, width, img):
    '''Dokonuje pomiaru obiektów na obrazie'''

    #wyznacza kontury
    contours = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    #usuwa kontury zbyt małych obiektów
    old_contours = list(contours)
    contours = []
    for contour in old_contours:
        if cv2.contourArea(contour) > 70:
            contours.append(contour)
            
    #oblicza stosunek pikseli do cm
    pixels_per_metric = calculatePixelsPerMetric(contours[int(choice)-1], width)

    #wyznacza prostokąty w których zawierają się obiekty
    for contour in contours:
        box = cv2.minAreaRect(contour)
        if imutils.is_cv2():
            box = cv2.cv.BoxPoints(box)
        else:
            box = cv2.boxPoints(box)
            
        box = np.array(box, dtype='int')
        box = perspective.order_points(box)

    
        #wyznacza środki boków tych prostokątów
        (top_left, top_right, bottom_right, bottom_left) = box
        (x1, y1) = midpoint(top_left, top_right)
        (x2, y2) = midpoint(bottom_left, bottom_right)
        (x3, y3) = midpoint(top_left, bottom_left)
        (x4, y4) = midpoint(top_right, bottom_right)

        #Odległości między środkami
        dA = distance.euclidean((x1, y1), (x2, y2))
        dB = distance.euclidean((x3, y3), (x4, y4))

        #Przeliczenie odległości na cm
        dimA = dA / pixels_per_metric
        dimB = dB / pixels_per_metric

        cv2.putText(img, "{:.3f}cm".format(dimB),
		(int(x1 - 15), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (255, 255, 255), 2)
        cv2.putText(img, "{:.3f}cm".format(dimA),
		(int(x4 + 10), int(y4)), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (255, 255, 255), 2)

        cv2.drawContours(img, [box.astype('int')], -1, (255, 0, 0), 2)

    return img

def calculatePixelsPerMetric(contours, width):
    '''Oblicza ilość pixeli na centymetr w oparciu o szerokość obiektu referencyjnego'''
    box = cv2.minAreaRect(contours)
        
    if imutils.is_cv2():
        box = cv2.cv.BoxPoints(box)
    else:
        box = cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    box = imutils.perspective.order_points(box)

    (top_left, top_right, bottom_right, bottom_left) = box
    (x3, y3) = midpoint(top_left, bottom_left)
    (x4, y4) = midpoint(top_right, bottom_right)
    dB = distance.euclidean((x3, y3), (x4, y4))

    return dB/width
        
def midpoint(A, B):
    '''Zwraca punkt będący środkiem odcinka AB'''
    return ((A[0] + B[0]) * 0.5, (A[1] + B[1]) * 0.5)