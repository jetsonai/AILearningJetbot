#!/usr/bin/env python

import rospy

from std_msgs.msg import String

rospy.init_node('topictest_pub')
# node name.

pub = rospy.Publisher('test_hello', String)
# topic name.

rate = rospy.Rate(2) #2 times per second

while not rospy.is_shutdown():
    pub.publish('Hello ROS')
    rate.sleep()

