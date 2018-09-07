import cv2
import numpy as np

#read image unchanged

#Car is approaching
orgimg = cv2.imread('eagle_2018_09_06_15_46_19_891.jpg',-1)

#Car is very close
#orgimg = cv2.imread('eagle_2018_09_06_15_46_20_321.jpg',-1)

#No cars ahead
#orgimg = cv2.imread('eagle_2018_09_06_15_46_07_743.jpg',-1)

#Car around the corner
#orgimg = cv2.imread('eagle_2018_09_06_15_46_09_867.jpg',-1)

#Hit front car
#orgimg = cv2.imread('eagle_2018_09_06_15_46_20_655.jpg',-1)

cv2.imshow('Original',orgimg)

img = cv2.bilateralFilter(orgimg,3,255,255)
lower_color = np.array([51, 51, 51])
upper_color = np.array([118, 143, 159])

imageObs = cv2.inRange(img, lower_color , upper_color)
clone = imageObs.copy()
_, cnts, _ = cv2.findContours(clone,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)
mask = np.zeros(img.shape[:2], dtype='uint8')
for c in cnts:
    cv2.drawContours(mask, [c], -1, 255, -1)

imageMask = cv2.bitwise_and(orgimg, orgimg, mask=mask)

cntObsNonZero = cv2.countNonZero(imageObs)
print cntObsNonZero

cv2.imshow('Frame',imageObs)
#cv2.imshow('Mask',imageMask)

imageObsLeft = imageObs[0:240, 0:80]
cv2.imshow('Left',imageObsLeft)

imageObsCentral = imageObs[0:240, 80:240]
cv2.imshow('Central',imageObsCentral)
cntObsCentralNonZero = cv2.countNonZero(imageObsCentral)
print cntObsCentralNonZero

imageObsRight = imageObs[0:240, 240:320]
cv2.imshow('Right',imageObsRight)

cv2.waitKey(0)
cv2.destroyAllWindows()

def detectObstacle(srcImg, bObsAhead, bObjOnLeft, bObjOnRight, nProximity):
    imgbiFilter = cv2.bilateralFilter(srcImg,3,255,255)
    #find grey colors
    lower_color = np.array([51, 51, 51])
    upper_color = np.array([118, 143, 159])

    imagePicked = cv2.inRange(imgbiFilter, lower_color , upper_color)
    clone = imagePicked.copy()
    _, cnts, _ = cv2.findContours(clone,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros(imgbiFilter.shape[:2], dtype='uint8')
    for c in cnts:
        cv2.drawContours(mask, [c], -1, 255, -1)    
