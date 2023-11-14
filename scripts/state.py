#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState

class State():
	def __init__(self): 
		rospy.init_node('State', anonymous=False)
		self.key_sub= rospy.Subscriber("/dynamixel_workbench/joint_states", \
			JointState, self.read)
		rate=rospy.Rate(1)
		while not rospy.is_shutdown():
			rospy.spin()

	def read(self,data):
		rospy.loginfo(data.position[0])

if __name__== "__main__": 
    try:
        State() 
    except: 
    	rospy.loginfo("End of the trip for Turtlesim") 