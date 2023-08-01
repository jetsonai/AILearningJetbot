#!/usr/bin/python3

# jetsonai@jetsonai.co.kr
# 20230415

import jetson.inference
import jetson.utils

import argparse
import sys

from Adafruit_MotorHAT import Adafruit_MotorHAT
import numpy as np

def set_speed(motor_ID, value):
    max_pwm = 115.0
    speed = int(min(max(abs(value * max_pwm), 0), max_pwm))

    if motor_ID == 3:
	    motor = motor_left
    elif motor_ID == 4:
	    motor = motor_right
    else:
	    return

    motor.setSpeed(speed)

    if value > 0:
	motor.run(Adafruit_MotorHAT.FORWARD)
    else:
        motor.run(Adafruit_MotorHAT.BACKWARD)

# stops all motors
def all_stop():
    motor_left.setSpeed(0)
    motor_right.setSpeed(0)

    motor_left.run(Adafruit_MotorHAT.RELEASE)
    motor_right.run(Adafruit_MotorHAT.RELEASE)


motor_driver = Adafruit_MotorHAT(i2c_bus=0)

motor_left_ID = 3
motor_right_ID = 4

motor_left = motor_driver.getMotor(motor_left_ID)
motor_right = motor_driver.getMotor(motor_right_ID)

print("motor_driver ready")

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.detectNet.Usage() +
                                 jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage())

parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 

is_headless = ["--headless"] if sys.argv[0].find('console.py') != -1 else [""]

try:
    opt = parser.parse_known_args()[0]
except:
    print("")
    parser.print_help()
    sys.exit(0)

# load the object detection network
net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)

# create video sources & outputs
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv+is_headless)

frameWidth = 640
speed_value = 0.3
turn_gain = 0.8
# process frames until the user exits
try:
    while True:
        # capture the next image
        img = input.Capture()

        # detect objects in the image (with overlay)
        detections = net.Detect(img, overlay=opt.overlay)

        # print the detections
        print("detected {:d} objects in image".format(len(detections)))

        for detection in detections:
		    #print(detection)
            if detection.ClassID == 17:
                #print('Center >> [0] %f, [1] %f' % (detection.Center[0], detection.Center[1])) 
                print('center pos >> [0] %f' % (detection.Center[0]))
                left_value = speed_value + turn_gain*(detection.Center[0]/frameWidth-0.5)
                right_value = speed_value - turn_gain*(detection.Center[0]/frameWidth-0.5)
                print(left_value)
                print(right_value)
                if left_value >= 0.48:
                    left_value = 0.48
                if right_value >= 0.48:
                    right_value = 0.48
                print('motor_value >> left %f, right %f' % (left_value, right_value))  
                set_speed(motor_left_ID,   left_value)
                set_speed(motor_right_ID,  right_value)
            else:
                all_stop()

        # render the image
        output.Render(img)

        # update the title bar
        output.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS()))

        # print out performance info
        net.PrintProfilerTimes()

        # exit on input/output EOS
        if not input.IsStreaming() or not output.IsStreaming():
            break

except KeyboardInterrupt:  
    print("key int")
    all_stop()

# When everything done, release the capture
all_stop()
