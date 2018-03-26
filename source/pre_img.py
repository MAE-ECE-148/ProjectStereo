import cv2
import time

LEFT_PATH = "/home/pi/images/left/{:06d}.jpg"
RIGHT_PATH = "/home/pi/images/right/{:06d}.jpg"

# TODO: Use more stable identifiers
left = cv2.VideoCapture(1)
right = cv2.VideoCapture(0)


CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720



# Increase the resolution
left.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
left.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
right.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
right.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    
# Use MJPEG to avoid overloading the USB 2.0 bus at this resolution
left.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
right.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))


frameId = 0
MAX_IMAGES = 10





CROP_WIDTH = 960
def cropHorizontal(image):
    return image[:,
            int((CAMERA_WIDTH-CROP_WIDTH)/2):
            int(CROP_WIDTH+(CAMERA_WIDTH-CROP_WIDTH)/2)]










# Grab both frames first, then retrieve to minimize latency between cameras
try:
    while(frameId <= MAX_IMAGES-1):
        if not (left.grab() and right.grab()):
            print("No more frames")
            break
        else:
            frameId+=1
            print("%d images left"%(MAX_IMAGES-frameId))
            
            
        _, leftFrame = left.retrieve()
        #leftFrame = cropHorizontal(leftFrame)
        _, rightFrame = right.retrieve()
        #rightFrame = cropHorizontal(rightFrame)

            
        cv2.imwrite(LEFT_PATH.format(frameId), leftFrame)
        cv2.imwrite(RIGHT_PATH.format(frameId), rightFrame)
        
        # cv2.imshow('left', leftFrame)
        # cv2.imshow('right', rightFrame)
    
    
        time.sleep(3)
    
    left.release()
    right.release()
    cv2.destroyAllWindows()   
        
        
        
except KeyboardInterrupt:
    left.release()
    right.release()
    cv2.destroyAllWindows()
        
        
        
    