#!/usr/bin/env python3
# USAGE
# python real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel
# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import numpy as np
import argparse
import imutils
import time
import cv2
import rospy
startX=0
startY=0
endX=0
endY=0
start_robot=0
max_size_X=0
max_size_Y=0
mean_dist_right=0
mean_dist_left=0
last_startX=0
last_endX=0
obstacle_detected=1
person_lost=0
idx=0
vel_msg=Twist()

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
print("[INFO] starting video stream...")
vs = VideoStream(src=3).start()
time.sleep(2.0)
fps = FPS().start()

def move_robot(obstacle_detected,person_lost):
	global vel_msg
	global startX
	global startY
	global endX
	global endY
	global last_endX
	global last_startX
	global vel_msg
	if person_lost==0:
		vel_msg.angular.z=-obstacle_detected*(((startX+endX)/400)-1)*1.2
		vel_msg.linear.x=((startY/8)-1)/30	
	elif person_lost==1:
		vel_msg.angular.z=0.3
		vel_msg.linear.x=0.1	
	else:
		vel_msg.angular.z=-0.3
		vel_msg.linear.x=0.1
	if vel_msg.linear.x>0.4:
		vel_msg.linear.x=0.4
	_cmd_pub.publish(vel_msg)
	if startX!=0 and endX!=0:
		last_endX=endX
		last_startX=startX
	return last_endX,last_startX

def laser_detection(data):
	Lengths = len(data.ranges)
	total_range_left=0.0
	total_range_right=0.0
	mean_dist_right=0.0
	mean_dist_left=0.0
	global obstacle_detected
	global vel_msg
	for i in range(0,242):
		if data.ranges[i]<0.5:
			total_range_right+=data.ranges[i]
	for i in range(484,726):
		if data.ranges[i]<0.5:
			total_range_left+=data.ranges[i]
	mean_dist_left=total_range_left/242
	mean_dist_right=total_range_right/242
	if (mean_dist_right>0.01 and mean_dist_right<0.16) or (mean_dist_left>0.01 and mean_dist_left<0.16) and vel_msg.angular.z>0.1 :
		obstacle_detected=0
	else:
		obstacle_detected=1
	return obstacle_detected


def person_recognition():
	global startX
	global startY
	global endX
	global endY
	global idx
	global person_lost
	global start_robot
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	# grab the frame dimensions and convert it to a blob
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
		0.007843, (300, 300), 127.5)

	# pass the blob through the network and obtain the detections and
	# predictions
	net.setInput(blob)
	detections = net.forward()

	
	if last_endX<200 and last_startX<50 and idx==0 and start_robot==1:
		person_lost=1
		move_robot(obstacle_detected,person_lost)
	elif last_endX>350 and last_startX>200 and idx==0 and start_robot==1:
		person_lost=2
		move_robot(obstacle_detected,person_lost)
	else:
		print("depart")

	# loop over the detections
	for i in np.arange(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the prediction
		confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the `confidence` is
		# greater than the minimum confidence
		if confidence > args["confidence"]:
			# extract the index of the class label from the
			# `detections`, then compute the (x, y)-coordinates of
			# the bounding box for the object
			idx = int(detections[0, 0, i, 1])
			#idx15 is the index of the person
			if idx==15:
				start_robot=1
				person_lost=0
				move_robot(obstacle_detected,person_lost)
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")
				# draw the prediction on the frame
				label = "{}: {:.2f}%".format(CLASSES[idx],
				confidence * 100)
				cv2.rectangle(frame, (startX, startY), (endX, endY),
				COLORS[idx], 2)
				y = startY - 15 if startY - 15 > 15 else startY + 15
				cv2.putText(frame, label, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
			else:
				idx=0

	# show the output frame
	cv2.imshow("Frame", frame)


	# update the FPS counter
	fps.update()
	
if __name__ == '__main__':
	rospy.init_node('person_tracking', anonymous=True)
	_cmd_pub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=1)
	rospy.Subscriber('/scan', LaserScan, laser_detection)
	while True:
		person_recognition()
		print("startx="+str(startX))
		print("endx="+str(endX))
		print("person_lost="+str(person_lost))
		print("idx="+str(idx))
		print("vitesse="+str(vel_msg.linear.x))
		print("angulaire="+str(vel_msg.angular.z))
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			fps.stop()
			cv2.destroyAllWindows()
			vs.stop()
