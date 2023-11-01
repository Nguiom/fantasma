#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class Moving(): 
	def __init__(self): 
		rospy.init_node('Moving', anonymous=False)
		self.cmd_vel = rospy.Publisher('/turtle1/cmd_vel',Twist, queue_size=10) 
		self.key_sub = rospy.Subscriber('key',String, self.judge)
		self.vel=Twist()
		rate=rospy.Rate(10)
		self.tabla={'w':(1,0),'s':(-1,0),'a':(0,1),'d':(0,-1)}
		while not rospy.is_shutdown():
			self.cmd_vel.publish(self.vel)
			rate.sleep()
	def judge(self,data):
		temp=self.tabla.get(data.data,(0,0))
		rospy.loginfo(temp)
		vx,wz=temp
		self.vel.linear.x=vx
		self.vel.linear.y=0
		self.vel.linear.z=0
		self.vel.angular.x=0
		self.vel.angular.y=0
		self.vel.angular.z=wz
if __name__== "__main__": 
	try:
		Moving() 
	except: 
		rospy.loginfo("End of the trip for Turtlesim") 
