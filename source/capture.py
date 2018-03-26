import numpy as np
import cv2
import sys
import calibrate

REMAP_INTERPOLATION = cv2.INTER_LANCZOS4

DEPTH_VISUALIZATION_SCALE = 2048
    
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720


    
    
   
# TODO: Use more stable identifiers
left = cv2.VideoCapture(1)
right = cv2.VideoCapture(0)
    
# Increase the resolution
left.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
left.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
right.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
right.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    
# Use MJPEG to avoid overloading the USB 2.0 bus at this resolution
left.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
right.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))


#stereoBM parameters
stereoMatcher = cv2.StereoBM_create(numDisparities=16, blockSize=15)
'''
stereoMatcher = cv2.StereoBM_create()

stereoMatcher.setMinDisparity(0)
stereoMatcher.setNumDisparities(32)
stereoMatcher.setBlockSize(9)
stereoMatcher.setSpeckleRange(0)
stereoMatcher.setSpeckleWindowSize(0)
'''


def cropHorizontal(image):
    
    # The distortion in the left and right edges prevents a good calibration, so
    # discard the edges
    CROP_WIDTH = 960
    
    return image[:,
            int((CAMERA_WIDTH-CROP_WIDTH)/2):
            int(CROP_WIDTH+(CAMERA_WIDTH-CROP_WIDTH)/2)]





def stereo_depth(imgL, imgR,leftMapX, leftMapY, rightMapX, rightMapY, leftROI, rightROI, imageSize):
    
    

    leftFrame=cv2.resize(imgL, (1280, 720), REMAP_INTERPOLATION)
    leftHeight, leftWidth = leftFrame.shape[:2]
    

    rightFrame=cv2.resize(imgR, (1280, 720), REMAP_INTERPOLATION)
    rightHeight, rightWidth = rightFrame.shape[:2]
    



    # TODO: Why these values in particular?
    # TODO: Try applying brightness/contrast/gamma adjustments to the images
    



    if (leftWidth, leftHeight) != imageSize:
        print("Left camera has different size than the calibration data")
        

    if (rightWidth, rightHeight) != imageSize:
        print("Right camera has different size than the calibration data")
        
    
    stereoMatcher.setROI1(leftROI)
    stereoMatcher.setROI2(rightROI)

    
    
    
    fixedLeft = cv2.remap(leftFrame, leftMapX, leftMapY, REMAP_INTERPOLATION)
    fixedRight = cv2.remap(rightFrame, rightMapX, rightMapY, REMAP_INTERPOLATION)
    
    
    cv2.imwrite("/home/pi/images/file_l.jpg",fixedLeft)
    cv2.imwrite("/home/pi/images/file_r.jpg", fixedRight)
    


    grayLeft = cv2.cvtColor(fixedLeft, cv2.COLOR_BGR2GRAY)
    grayRight = cv2.cvtColor(fixedRight, cv2.COLOR_BGR2GRAY)
    
    
    depth = stereoMatcher.compute(grayLeft, grayRight)
    #depth = cv2.resize(depth, (160, 120), REMAP_INTERPOLATION) 
       
    
    # cv2.imshow('left', fixedLeft)
    # cv2.imshow('right', fixedRight)
    # cv2.imshow('depth', depth / DEPTH_VISUALIZATION_SCALE)
    
    return depth
    


leftMapX, leftMapY,rightMapX, rightMapY, leftROI, rightROI, imageSize= calibrate.calibrate()
print(imageSize)
left.grab()
right.grab()
_,imgL=left.retrieve()
_,imgR=right.retrieve()
depth=stereo_depth(imgL, imgR,leftMapX, leftMapY, rightMapX, rightMapY, leftROI, rightROI, imageSize)
cv2.imwrite("/home/pi/images/depth.jpg", depth)    
   
    