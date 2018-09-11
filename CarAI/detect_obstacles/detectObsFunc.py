import cv2
import numpy as np

def isAnyObstacleInFrontView(nPixels):
    if nPixels <= 550:
        return False
    else:
        return True

def isAnyObstacleOnLeftRightView(nPixels):
    if nPixels <= 260:
        return False
    else:
        return True
    
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
        
def detectObstacle(srcImg):
    imgbiFilter = cv2.bilateralFilter(srcImg,3,255,255)
    #find grey colors
    lower_color = np.array([51, 51, 51])
    upper_color = np.array([118, 143, 159])

    imagePicked = cv2.inRange(imgbiFilter, lower_color , upper_color)

    #cntPickedNonZero = cv2.countNonZero(imagePicked)
    #print('ImgPicked non-zero: ' + str(cntPickedNonZero))
    cv2.imshow('Obstacle', imagePicked)

    imagePickedLeft = imagePicked[0:240, 0:80]
    #cv2.imshow('Obj Left',imagePickedLeft)
    cntPickedLeftNonZero = cv2.countNonZero(imagePickedLeft)
    bObjOnLeft = isAnyObstacleOnLeftRightView(cntPickedLeftNonZero)
    print('Obj Left: ' + str(cntPickedLeftNonZero))
    
    imagePickedCentral = imagePicked[0:240, 80:240]
    #cv2.imshow('Obj Central',imagePickedCentral)
    cntPickedCentralNonZero = cv2.countNonZero(imagePickedCentral)
    bObsAhead = isAnyObstacleInFrontView(cntPickedCentralNonZero)
    print('Obj Central: ' + str(cntPickedCentralNonZero))

    imagePickedRight = imagePicked[0:240, 240:320]
    #cv2.imshow('Obj Right',imagePickedRight)
    cntPickedRightNonZero = cv2.countNonZero(imagePickedRight)
    bObjOnRight = isAnyObstacleOnLeftRightView(cntPickedRightNonZero)
    print('Obj Right: ' + str(cntPickedRightNonZero))
    
    return bObsAhead, bObjOnLeft, bObjOnRight

def detectWall(srcImg, tgtColor):
    imgbiFilter = cv2.bilateralFilter(srcImg,3,255,255)
    #Pick nearly black
    lower_color = np.array([0, 0, 0])
    upper_color = np.array([20, 20, 20])

    if tgtColor == 1:
            lower_color = np.array([0, 165, 165])
            upper_color = np.array([15, 177, 178])
            
    imagePicked = cv2.inRange(imgbiFilter, lower_color , upper_color)
    #black the top of image to ignore sign bar
    imagePicked[0:70, 0:320] = 0    
    if tgtColor == 0:
        cv2.imshow('Black Wall',imagePicked)
    elif tgtColor == 1:
        cv2.imshow('Yellow-Green Wall',imagePicked)
        
    imagePickedLeft = imagePicked[0:240, 0:80]
    #cv2.imshow('Wall Left',imagePickedLeft)
    cntPickedLeftNonZero = cv2.countNonZero(imagePickedLeft)
    bWallOnLeft = isAnyWallOnLeftRightView(cntPickedLeftNonZero)
    print('Wall Left: ' + str(cntPickedLeftNonZero))

    imagePickedCentral = imagePicked[0:240, 80:240]
    #cv2.imshow('Wall Central',imagePickedCentral)
    cntPickedCentralNonZero = cv2.countNonZero(imagePickedCentral)
    bWallAhead = isAnyWallInFrontView(cntPickedCentralNonZero)
    print('Wall Central: ' + str(cntPickedCentralNonZero))

    imagePickedRight = imagePicked[0:240, 240:320]
    #cv2.imshow('Wall Right',imagePickedRight)
    cntPickedRightNonZero = cv2.countNonZero(imagePickedRight)
    bWallOnRight = isAnyWallOnLeftRightView(cntPickedRightNonZero)
    print('Wall Right: ' + str(cntPickedRightNonZero))
    
    return bWallAhead, bWallOnLeft, bWallOnRight

#Car is approaching
#orgimg = cv2.imread('eagle_2018_09_06_15_46_19_891.jpg',-1)

#Car is very close
#orgimg = cv2.imread('eagle_2018_09_06_15_46_20_321.jpg',-1)

#No cars ahead, Wall and Signs
#orgimg = cv2.imread('eagle_2018_09_06_15_46_07_743.jpg',-1)

#Car around the corner
#orgimg = cv2.imread('eagle_2018_09_06_15_46_09_867.jpg',-1)

#Hit front car
#orgimg = cv2.imread('eagle_2018_09_06_15_46_20_655.jpg',-1)

#Wll and Car
#orgimg = cv2.imread('eagle_2018_09_06_15_46_19_891.jpg',-1)

#Big Wall
#orgimg = cv2.imread('eagle_2018_09_06_15_46_10_902.jpg',-1)

#Wll and Car
#orgimg = cv2.imread('eagle_2018_09_06_15_46_19_060.jpg',-1)

#Wrong judgment due to pixel thread 175 (change to 200)
#orgimg = cv2.imread('obs_1002.jpg',-1)

#Wrong judgment due to sign bar above the road (change to 200)
#orgimg = cv2.imread('wall_2004.jpg',-1)

#Detect yellow-green wall
orgimg = cv2.imread('eagle_2018_09_11_23_15_53_994.jpg',-1)

bObsAhead, bObjOnLeft, bObjOnRight = detectObstacle(orgimg)
print('Car Ahead: ' + str(bObsAhead))
print('Car on the left: ' + str(bObjOnLeft))
print('Car on the right: ' + str(bObjOnRight))

bBkWallAhead, bBkWallOnLeft, bBkWallOnRight = detectWall(orgimg, 0)
print('Black Wall Ahead: ' + str(bBkWallAhead))
print('Black Wall on the left: ' + str(bBkWallOnLeft))
print('Black Wall on the right: ' + str(bBkWallOnRight))

bYgWallAhead, bYgWallOnLeft, bYgWallOnRight = detectWall(orgimg, 1)
print('Yellow-Green Wall Ahead: ' + str(bYgWallAhead))
print('Yellow-Green on the left: ' + str(bYgWallOnLeft))
print('Yellow-Green on the right: ' + str(bYgWallOnRight))

cv2.waitKey(0)
cv2.destroyAllWindows()
