#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import TeleportAbsolute, TeleportRelative
from std_msgs.msg import String

class Teleport():
	def __init__(self): 
		rospy.init_node('Teleport', anonymous=False)
		self.key_sub= rospy.Subscriber('key',String, self.update_key)
		self.key=0
		self.cont=True
		self.tabla={' ':(1),'r':(2)}
		rate=rospy.Rate(10)
		while not rospy.is_shutdown():
			if(self.key==1 and self.cont):
				self.teleportA()
				self.cont=False
			elif(self.key==2 and self.cont):
				self.teleportR()
				self.cont=False
			elif(self.key==0):
				self.cont=True
			rate.sleep()
	def teleportA(self):
		rospy.wait_for_service('/turtle1/teleport_absolute')
		try:
			teleportA = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
			resp1 = teleportA(5, 5, 0)
		except rospy.ServiceException as e:
			print(str(e))
	def teleportR(self):
		rospy.wait_for_service('/turtle1/teleport_relative')
		try:
			teleportR = rospy.ServiceProxy('/turtle1/teleport_relative', TeleportRelative)
			resp1 = teleportR(0,3.1416)
		except rospy.ServiceException as e:
			print(str(e))
	def update_key(self,data):
		self.key=self.tabla.get(data.data,(0))

if __name__== "__main__": 
    try:
        Teleport() 
    except: 
    	rospy.loginfo("End of the trip for Turtlesim") 