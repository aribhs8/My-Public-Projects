# import openCV and numpy modules
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# setup detectors and parameters
params = cv2.SimpleBlobDetector_Params()

params.filterByColor = False
params.filterByArea = True
params.minArea = 20000
params.maxArea = 30000
params.filterByInertia = False
params.filterByConvexity = False
params.filterByCircularity = True
params.minCircularity = 0.5
params.maxCircularity = 1

det = cv2.SimpleBlobDetector_create(params)

# define blue
lower_yellow = np.array([30, 120, 120])
upper_yellow = np.array([40, 255, 255])

while True:
	ret, frame = cap.read()
	
	imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	
	yellowMask = cv2.inRange(imgHSV, lower_yellow, upper_yellow)
	blur = cv2.blur(yellowMask, (10,10))
	
	res = cv2.bitwise_and(frame, frame, mask=yellowMask)
	
	# get and draw keypoints
	keypoints = det.detect(blur)
	
	cv2.drawKeypoints(frame, keypoints, frame, (0,0,255), 
						cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
						
	cv2.imshow('frame', frame)
	cv2.imshow('mask', blur)
	
	for k in keypoints:
		print k.size
	
	if cv2.waitKey(1) & 0xff == ord('q'):
		break
		
cap.release()
cv2.destroyAllWindows()
