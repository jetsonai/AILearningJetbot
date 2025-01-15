#!/usr/bin/env python

import rospy

from std_msgs.msg import String

def callback(msg):  # callback function
    print msg.data

rospy.init_node('topictest_sub')
# node name

sub = rospy.Subscriber('test_hello', String, callback)
# register callback

rospy.spin()
# give control to ROS


