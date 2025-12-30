import time
import argparse
import cv2 as cv
import numpy as np
import pywhatkit as kit
from Pose.pose_visualizer import TfPoseVisualizer
from Action.recognizer import load_action_premodel, framewise_recognize
from utils import choose_run_mode, load_pretrain_model, set_video_writer

phone_number = "+91 XXXXX XXXXX"
message = "Alert: Your child experienced a minor fall. Immediate attention required"

parser = argparse.ArgumentParser(description='Action Recognition by OpenPose')
parser.add_argument('--video', help='Path to video file.')
args = parser.parse_args()

estimator = load_pretrain_model('VGG_origin')
action_classifier = load_action_premodel('Action/framewise_recognition_under_scene.h5')

realtime_fps = '0.0000'
start_time = time.time()
fps_interval = 1
fps_count = 0
run_timer = 0
frame_count = 0

cap = choose_run_mode(args)
print(args.video)
video_writer = set_video_writer(cap, write_fps=int(7.0))
send = False

while cv.waitKey(1) < 0:
    has_frame, show = cap.read()
    if has_frame:
        fps_count += 1
        frame_count += 1
        print(show.shape)
        
        humans = estimator.inference(show)
        pose = TfPoseVisualizer.draw_pose_rgb(show, humans)  
        show,label = framewise_recognize(pose, action_classifier,args.video,frame_count)

        height, width = show.shape[:2]
        if (time.time() - start_time) > fps_interval:
            realtime_fps = fps_count / (time.time() - start_time)
            fps_count = 0  
            start_time = time.time()
        fps_label = 'FPS:{0:.2f}'.format(float(realtime_fps))

        num_label = "Human: {0}".format(len(humans))
        cv.putText(show, num_label, (5, height-45), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

        if frame_count == 1:
            run_timer = time.time()
        run_time = time.time() - run_timer
        time_frame_label = '[Time:{0:.2f} | Frame:{1}]'.format(run_time, frame_count)
        cv.putText(show, time_frame_label, (width-500, 25), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

        cv.imshow('Action Recognition based on OpenPose', show)
        if frame_count > 50:
            if label == 'fall_down' and send==False:
                cv.imwrite('img_2.jpg',show)
                send = True
                kit.sendwhatmsg_instantly(phone_number, message)
                kit.sendwhats_image(phone_number, "img_2.jpg")
            
        video_writer.write(show)


video_writer.release()
cap.release()