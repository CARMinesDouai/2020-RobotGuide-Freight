#!/usr/bin/env python3
# Code Anis - Defend Intelligence
import cv2
import dlib
import PIL.Image
import numpy as np
from std_msgs.msg import Bool
from imutils import face_utils
import imutils
import argparse
from pathlib import Path
import os
import ntpath
import rospy
import pyrealsense2 as rs
import numpy as np
import rospkg
from person_following.msg import person_presence
from projet_fetch.msg import capture

essai=False
top=0
left=0
right=0
bottom=0
dist_total_average=0
person_pres=person_presence()
person_pres.Distance=0
person_pres.Presence=False
increment=0
counter_missing=0
face_locations=0
coord_faces = [(0,0,0,0)]
name=''
face_capture=capture()
face_capture.take_capture=False
face_save=False


rospack = rospkg.RosPack()
packagePath=rospack.get_path('person_following')
print('[INFO] Starting System...')
print('[INFO] Importing pretrained model..')
pose_predictor_68_point = dlib.shape_predictor(str(packagePath)+"/scripts/pretrained_model/shape_predictor_68_face_landmarks.dat")
pose_predictor_5_point = dlib.shape_predictor(str(packagePath)+"/scripts/pretrained_model/shape_predictor_5_face_landmarks.dat")
face_encoder = dlib.face_recognition_model_v1(str(packagePath)+"/scripts/pretrained_model/dlib_face_recognition_resnet_model_v1.dat")
face_detector = dlib.get_frontal_face_detector()
face_recon = False
print('[INFO] Importing pretrained model..')

def wait_for_capture(data):
    global face_capture
    face_capture.take_capture=data.take_capture

def transform(image, face_locations):
    global coord_faces
    coord_faces = [(0,0,0,0)]
    for face in face_locations:
        rect = face.top(), face.right(), face.bottom(), face.left()
        coord_face = max(rect[0], 0), min(rect[1], image.shape[1]), min(rect[2], image.shape[0]), max(rect[3], 0)
        coord_faces[0]=coord_face
    return coord_faces

def encode_face(image):
    global face_locations
    face_locations = face_detector(image, 1)
    face_encodings_list = []
    landmarks_list=[]
    for face_location in face_locations:
        # DETECT FACES
        shape = pose_predictor_68_point(image, face_location)
        face_encodings_list.append(np.array(face_encoder.compute_face_descriptor(image, shape, num_jitters=1)))
        # GET LANDMARKS
        shape = face_utils.shape_to_np(shape)
        landmarks_list.append(shape)
    face_locations = transform(image, face_locations)
    return face_encodings_list, face_locations, landmarks_list


def easy_face_reco(frame, known_face_encodings, known_face_names):
    global increment
    global top
    global bottom
    global right
    global left
    global person_pres
    global dist_total_average
    global name
    top=0
    left=0
    right=0
    bottom=0
    rgb_small_frame = frame[:, :, ::-1]
    # ENCODING FACE
    face_encodings_list, face_locations_list, landmarks_list = encode_face(rgb_small_frame)
    face_names = []
    for face_encoding in face_encodings_list:
        if len(face_encoding) == 0:
            return np.empty((0))
        # CHECK DISTANCE BETWEEN KNOWN FACES AND FACES DETECTED
        vectors = np.linalg.norm(known_face_encodings - face_encoding, axis=1)
        tolerance = 0.6
        result = []
        for vector in vectors:
            if vector <= tolerance:
                result.append(True)
            else:
                result.append(False)
        if True in result:
            first_match_index = result.index(True)
            name = known_face_names[first_match_index]
            face_recon = True
            person_pres.Presence=True
        else:
            name = "Unknown"
        face_names.append(name)
    for (top, right, bottom, left), name in zip(face_locations_list, face_names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 30), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 2, bottom - 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)

def distance_person(depth_frame):
	global person_pres
	global top
	global left
	global right
	global bottom
	dist_total_average=0
	dist_total=0
	top=top+50
	bottom=bottom-50
	left=left+50
	right=right-50
	for height in range (top,bottom):
                divided=0
                dist_line=0
                for width in range(left,right):
                        if depth_frame.get_distance(width,height)>0 and depth_frame.get_distance(width,height)<3:                               
                                dist_line+=depth_frame.get_distance(width,height) 
                                divided+=1
                if divided!=0:
                        dist_total+=dist_line/(divided)
        
	dist_total_average=100*(dist_total/(bottom-top))
	person_pres.Distance=int(dist_total_average)
	return dist_total_average

	

if __name__ == '__main__':
    rospy.init_node("facial_recognition",anonymous=True)
    _cmd_pub=rospy.Publisher("/person_following",person_presence,queue_size=1)
    rospy.Subscriber("/face_capture",capture, wait_for_capture)
    print('[INFO] Importing faces...')
    known_faces_path=str(packagePath)+"/scripts/known_faces/"
    face_to_encode_path = Path(known_faces_path)
    files = [file_ for file_ in face_to_encode_path.rglob('*.jpg')]

    for file_ in face_to_encode_path.rglob('*.png'):
        files.append(file_)
    if len(files)==0:
        raise ValueError('No faces detect in the directory: {}'.format(face_to_encode_path))
    known_face_names = [os.path.splitext(ntpath.basename(file_))[0] for file_ in files]

    known_face_encodings = []
    for file_ in files:
        image = PIL.Image.open(file_)
        image = np.array(image)
        face_encoded = encode_face(image)[0][0]
        known_face_encodings.append(face_encoded)

    print('[INFO] Faces well imported')
    print('[INFO] Starting Webcam...')
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    pipeline.start(config)
    print('[INFO] Webcam well started')
    print('[INFO] Detecting...')
    print('[INFO] Photo Waiting')
    while not rospy.is_shutdown():
        while not face_save:
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame().as_depth_frame()
            color_frame = frames.get_color_frame()
            color_image = np.asanyarray(color_frame.get_data())
            if face_capture.take_capture:
                crop_image=color_image[160:480,0:480]
                cv2.imwrite(str(packagePath)+"/scripts/known_faces/image.jpg",crop_image)
                cv2.imshow('image_save',crop_image)
                face_save=True
                print('[INFO] Let''s started')
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame().as_depth_frame()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        easy_face_reco(color_image, known_face_encodings, known_face_names)
        #cv2.imshow('Easy Facial Recognition App', color_image)
        if coord_faces[0][0]==0 or name=="Unknown":
            counter_missing+=1
        else:
            counter_missing=0
        if counter_missing>20:
            person_pres.Presence=False
        _cmd_pub.publish(person_pres)
    print('[INFO] Stopping System')
    pipeline.stop()
    cv2.destroyAllWindows()
