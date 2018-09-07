import cv2
import numpy as np

def isAnyObstacleIntheView(nPixels):
    if nPixels <= 175:
        return False
    else:
        return True
    
def detectObstacle(srcImg):
    imgbiFilter = cv2.bilateralFilter(srcImg,3,255,255)
    #find grey colors
    lower_color = np.array([51, 51, 51])
    upper_color = np.array([118, 143, 159])

    imagePicked = cv2.inRange(imgbiFilter, lower_color , upper_color)

    cntPickedNonZero = cv2.countNonZero(imagePicked)
    print('ImgPicked non-zero: ' + str(cntPickedNonZero))
    cv2.imshow('Image Picked', imagePicked)

    imagePickedLeft = imagePicked[0:240, 0:80]
    cv2.imshow('Left',imagePickedLeft)
    cntPickedLeftNonZero = cv2.countNonZero(imagePickedLeft)
    bObjOnLeft = isAnyObstacleIntheView(cntPickedLeftNonZero)
    print('Left non-zero: ' + str(cntPickedLeftNonZero))
    
    imagePickedCentral = imagePicked[0:240, 80:240]
    cv2.imshow('Central',imagePickedCentral)
    cntPickedCentralNonZero = cv2.countNonZero(imagePickedCentral)
    bObsAhead = isAnyObstacleIntheView(cntPickedCentralNonZero)
    print('Central non-zero: ' + str(cntPickedCentralNonZero))

    imagePickedRight = imagePicked[0:240, 240:320]
    cv2.imshow('Right',imagePickedRight)
    cntPickedRightNonZero = cv2.countNonZero(imagePickedRight)
    bObjOnRight = isAnyObstacleIntheView(cntPickedRightNonZero)
    print('Right non-zero: ' + str(cntPickedRightNonZero))
    
    nProximity = 0
    return bObsAhead, bObjOnLeft, bObjOnRight, nProximity

#Car is approaching
print('Car is approaching')
orgimg = cv2.imread('eagle_2018_09_06_15_46_19_891.jpg',-1)

#Car is very close
#print('Car is quite close')    
#orgimg = cv2.imread('eagle_2018_09_06_15_46_20_321.jpg',-1)

#No cars ahead
#print('No cars ahead')    
#orgimg = cv2.imread('eagle_2018_09_06_15_46_07_743.jpg',-1)

#Car around the corner
#print('Car around the corner')    
#orgimg = cv2.imread('eagle_2018_09_06_15_46_09_867.jpg',-1)

#Hit front car
#print('Hit front car')        
#orgimg = cv2.imread('eagle_2018_09_06_15_46_20_655.jpg',-1)

bObsAhead, bObjOnLeft, bObjOnRight, nProximity = detectObstacle(orgimg)
print('Car in front of us: ' + str(bObsAhead))
print('Car on the left: ' + str(bObjOnLeft))
print('Car on the right: ' + str(bObjOnRight))

cv2.waitKey(0)
cv2.destroyAllWindows()
