#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from dynamixel_workbench_msgs.srv import DynamixelCommand
import numpy as np

class Moving(): 
	def __init__(self): 
		rospy.init_node('Moving', anonymous=False)
		self.key_sub = rospy.Subscriber('key',String, self.judge)
		self.rate=rospy.Rate(0.5)
		self.key=[500,500,500,500]
		self.tabla={'q':self.interpret(150,150,150,150),'w':self.interpret(175,175,170,130),\
			'e':self.interpret(115,185,120,180),'r':self.interpret(235,130,205,175),\
				't':self.interpret(230,115,205,115)}
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
		self.key=self.tabla.get(data.data,self.key)

		rospy.loginfo(temp)
	def interpret(self,a,b,c,d):
		ans=[]
		ans.append(np.interp(a,[0,300],[0,1022]))
		ans.append(np.interp(b,[0,300],[0,1022]))
		ans.append(np.interp(c,[0,300],[0,1022]))
		ans.append(np.interp(d,[0,300],[0,1022]))
		return ans
if __name__== "__main__": 
	try:
		temp=Moving()
		temp.jointCommand('', 1, 'Torque_Limit', 500, 0.5)
		temp.jointCommand('', 2, 'Torque_Limit', 500, 0.5)
		temp.jointCommand('', 3, 'Torque_Limit', 400, 0.5)
		temp.jointCommand('', 4, 'Torque_Limit', 400, 0.5)
		while not rospy.is_shutdown():
			temp.jointCommand('',1,'Goal_Position',temp.key[0], 0.5)
			temp.jointCommand('',2,'Goal_Position',temp.key[1], 0.5)
			temp.jointCommand('',3,'Goal_Position',temp.key[2], 0.5)
			temp.jointCommand('',4,'Goal_Position',temp.key[3], 0.5)
			temp.rate.sleep()
	except: 
		rospy.loginfo("End of the trip for Turtlesim") 
