#!/usr/bin/env python

import rospy
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from dynamixel_workbench_msgs.srv import DynamixelCommand
import numpy as np

class Moving(): 
	def __init__(self): 
		rospy.init_node('Moving', anonymous=False)
		self.goal_serve = rospy.Service('goal',numpy_msg(Floats), self.judge)
		self.rate=rospy.Rate(1)
		self.goal=[500,500,500,500]
	def jointCommand(self,command, id_num, addr_name, value, time):
		rospy.wait_for_service('dynamixel_workbench/dynamixel_command')
		try:        
			dynamixel_command = rospy.ServiceProxy(
            	'/dynamixel_workbench/dynamixel_command', DynamixelCommand)
			result = dynamixel_command(command,id_num,addr_name,value)
			return result.comm_result
		except rospy.ServiceException as exc:
				print(str(exc))
	def judge(self,data):
		self.goal[0]=int(np.interp(data[0]+150[0,300],[0,1022]))
		self.goal[1]=int(np.interp(data[1]+150,[0,300],[0,1022]))
		self.goal[2]=int(np.interp(data[2]+150,[0,300],[0,1022]))
		self.goal[3]=int(np.interp(data[3]+150,[0,300],[0,1022]))
		self.jointCommand('',1,'Goal_Position',self.goal[0], 0.5)
		self.jointCommand('',2,'Goal_Position',self.goal[1], 0.5)
		self.jointCommand('',3,'Goal_Position',self.goal[2], 0.5)
		self.jointCommand('',4,'Goal_Position',self.goal[3], 0.5)
		self.rate.sleep()

if __name__== "__main__": 
	try:
		temp=Moving()
	except: 
		rospy.loginfo("End of the trip for Robotica 2023-2") 
