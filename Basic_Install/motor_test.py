import time

from Adafruit_MotorHAT import Adafruit_MotorHAT
import time

# sets motor speed between [-1.0, 1.0]
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




# setup motor controller
motor_driver = Adafruit_MotorHAT(i2c_bus=0)

motor_left_ID = 3
motor_right_ID = 4

motor_left = motor_driver.getMotor(motor_left_ID)
motor_right = motor_driver.getMotor(motor_right_ID)

set_speed(motor_left_ID,   0.5)
set_speed(motor_right_ID,  0.5)

time.sleep(3.0)

# stop the motors as precaution
all_stop()

