import cv2
import numpy as np

obs_img_serial_number = 1000
wall_img_serial_number = 2000

def rsWriteLog(msg):
    '''
    with open('detectObjWall.log', 'a') as log_file:
        log_file.write(msg + '\n')
    '''
    dummy = 0
    
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
    global obs_img_serial_number
    imgbiFilter = cv2.bilateralFilter(srcImg,3,255,255)
    #find grey colors
    lower_color = np.array([51, 51, 51])
    upper_color = np.array([118, 143, 159])

    imagePicked = cv2.inRange(imgbiFilter, lower_color , upper_color)

    imagePickedLeft = imagePicked[0:240, 0:80]
    cntPickedLeftNonZero = cv2.countNonZero(imagePickedLeft)
    bObjOnLeft = isAnyObstacleOnLeftRightView(cntPickedLeftNonZero)
    #print('Obj Left: ' + str(cntPickedLeftNonZero))
    
    imagePickedCentral = imagePicked[0:240, 80:240]
    cntPickedCentralNonZero = cv2.countNonZero(imagePickedCentral)
    bObsAhead = isAnyObstacleInFrontView(cntPickedCentralNonZero)
    #print('Obj Central: ' + str(cntPickedCentralNonZero))

    imagePickedRight = imagePicked[0:240, 240:320]
    cntPickedRightNonZero = cv2.countNonZero(imagePickedRight)
    bObjOnRight = isAnyObstacleOnLeftRightView(cntPickedRightNonZero)
    #print('Obj Right: ' + str(cntPickedRightNonZero))

    if bObsAhead == True:
        out_img_filename = 'Obs_' + str(obs_img_serial_number) + '.jpg'
        obs_img_serial_number = obs_img_serial_number + 1
        #cv2.imwrite(out_img_filename, srcImg)

    return bObsAhead, bObjOnLeft, bObjOnRight

def detectWall(srcImg):
    global wall_img_serial_number
    imgbiFilter = cv2.bilateralFilter(srcImg,3,255,255)
    #Pick nearly black
    lower_color = np.array([0, 0, 0])
    upper_color = np.array([20, 20, 20])

    imagePicked = cv2.inRange(imgbiFilter, lower_color , upper_color)
    #black the top of image to ignore sign bar
    imagePicked[0:70, 0:320] = 0
    
    imagePickedLeft = imagePicked[0:240, 0:80]
    cntPickedLeftNonZero = cv2.countNonZero(imagePickedLeft)
    bWallOnLeft = isAnyWallOnLeftRightView(cntPickedLeftNonZero)
    #print('Wall Left: ' + str(cntPickedLeftNonZero))

    imagePickedCentral = imagePicked[0:240, 80:240]
    cntPickedCentralNonZero = cv2.countNonZero(imagePickedCentral)
    bWallAhead = isAnyWallInFrontView(cntPickedCentralNonZero)
    #print('Wall Central: ' + str(cntPickedCentralNonZero))

    imagePickedRight = imagePicked[0:240, 240:320]
    cntPickedRightNonZero = cv2.countNonZero(imagePickedRight)
    bWallOnRight = isAnyWallOnLeftRightView(cntPickedRightNonZero)
    #print('Wall Right: ' + str(cntPickedRightNonZero))
       
    if bWallAhead == True:
        out_img_filename = 'Wall_' + str(wall_img_serial_number) + '.jpg'
        wall_img_serial_number = wall_img_serial_number + 1
        #cv2.imwrite(out_img_filename, srcImg)
     
    return bWallAhead, bWallOnLeft, bWallOnRight

def steeringAdjustment(bObsAhead, bObjOnLeft, bObjOnRight, bWallAhead, bWallOnLeft, bWallOnRight):
    #if there is nothing ahead
    nRet = 0
    if bObsAhead == False and bWallAhead == False:
        nRet = 0
    
    #Something ahead, can we steer right?
    elif bObjOnRight == False and bWallOnRight == False:
        nRet = 1
        
    #Something ahead and on the right, can we steer left?
    elif bObjOnRight == False and bWallOnRight == False:
        nRet = -1

    #We can't turn right and left, do nothing
    else:
        nRet = 0

    return nRet
