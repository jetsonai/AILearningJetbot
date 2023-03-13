import jetson.inference
import jetson.utils
from Adafruit_MotorHAT import Adafruit_MotorHAT
import numpy as np

def set_speed(motor_ID, value):
	max_pwm = 115.0
	speed = int(min(max(abs(value * max_pwm), 0), max_pwm))

	if motor_ID == 1:
		motor = motor_left
	elif motor_ID == 2:
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


motor_driver = Adafruit_MotorHAT(i2c_bus=1)

motor_left_ID = 1
motor_right_ID = 2

motor_left = motor_driver.getMotor(motor_left_ID)
motor_right = motor_driver.getMotor(motor_right_ID)

print("motor_driver ready")

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson.utils.videoSource("csi://0")      # '/dev/video0' for V4L2
display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file

speed_value = 0.3
turn_gain = 0.8

try:
    while display.IsStreaming():
        img = camera.Capture()
        detections = net.Detect(img)
        for detection in detections:
            #print(detection.ClassID) print(detection.Confidence)
            #print(detection.Left)print(detection.Top)
            #print(detection.Width)print(detection.Height)
            if detection.ClassID == 1:
                #print('Center >> [0] %f, [1] %f' % (detection.Center[0], detection.Center[1])) 
                print('Center >> [0] %f' % (detection.Center[0]))
                left_value = speed_value + turn_gain*(detection.Center[0]/224-0.5)
                right_value = speed_value - turn_gain*(detection.Center[0]/224-0.5)
                if left_value >= 0.48:
                    left_value = 0.48
                if right_value >= 0.48:
                    right_value = 0.48
                print('motor_value >> left %f, right %f' % (left_value, right_value))  
                set_speed(motor_left_ID,   left_value)
                set_speed(motor_right_ID,  right_value)
            else:
                all_stop()

	        #print(detection)
        display.Render(img)
        display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

except KeyboardInterrupt:  
    print("key int")
    all_stop()

# When everything done, release the capture
all_stop()
