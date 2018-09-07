import cv2
import numpy as np

def isAnyWallInFrontView(nPixels):
    if nPixels <= 5000:
        return False
    else:
        return True

def isAnyWallOnLeftRightView(nPixels):
    if nPixels <= 3300:
        return False
    else:
        return True
    
#Wall and Signs
#orgimg = cv2.imread('eagle_2018_09_06_15_46_07_743.jpg',-1)

#Wll and Car
#orgimg = cv2.imread('eagle_2018_09_06_15_46_19_891.jpg',-1)

#Big Wall
#orgimg = cv2.imread('eagle_2018_09_06_15_46_10_902.jpg',-1)

#Car is very close
#orgimg = cv2.imread('eagle_2018_09_06_15_46_20_321.jpg',-1)

#Big open
#orgimg = cv2.imread('eagle_2018_09_06_15_46_09_867.jpg',-1)

#Hit front car
#orgimg = cv2.imread('eagle_2018_09_06_15_46_20_655.jpg',-1)

orgimg = cv2.imread('wall_2000.jpg',-1)

cv2.imshow('Original',orgimg)

imgbiFilter = cv2.bilateralFilter(orgimg,3,255,255)
lower_color = np.array([0, 0, 0])
upper_color = np.array([20, 20, 20])

imagePicked = cv2.inRange(imgbiFilter, lower_color , upper_color)
#black the top of image to ignore sign bar
imagePicked[0:70, 0:320] = 0
cv2.imshow('Wall',imagePicked)

imagePickedLeft = imagePicked[0:240, 0:80]
cv2.imshow('Left',imagePickedLeft)
cntPickedLeftNonZero = cv2.countNonZero(imagePickedLeft)
bObjOnLeft = isAnyWallOnLeftRightView(cntPickedLeftNonZero)
print('Left non-zero: ' + str(cntPickedLeftNonZero))

imagePickedCentral = imagePicked[0:240, 80:240]
cv2.imshow('Central',imagePickedCentral)
cntPickedCentralNonZero = cv2.countNonZero(imagePickedCentral)
bObsAhead = isAnyWallInFrontView(cntPickedCentralNonZero)
print('Central non-zero: ' + str(cntPickedCentralNonZero))

imagePickedRight = imagePicked[0:240, 240:320]
cv2.imshow('Right',imagePickedRight)
cntPickedRightNonZero = cv2.countNonZero(imagePickedRight)
bObjOnRight = isAnyWallOnLeftRightView(cntPickedRightNonZero)
print('Right non-zero: ' + str(cntPickedRightNonZero))

print('Wall in front of us: ' + str(bObsAhead))
print('Wall on the left: ' + str(bObjOnLeft))
print('Wall on the right: ' + str(bObjOnRight))

cv2.waitKey(0)
cv2.destroyAllWindows()
