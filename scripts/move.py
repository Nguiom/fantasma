#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32MultiArray
from dynamixel_workbench_msgs.srv import DynamixelCommand
import numpy as np

class Moving(): 
	def __init__(self): 
		rospy.init_node('Moving', anonymous=False)
		self.goal_serve = rospy.Service('move',Int32MultiArray, self.judge)
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
		pos1=np.array([data[0],data[1],data[2]])
		pos2=np.array([data[3],data[4],data[5]])
		q1,q2,q3,q4=self.makeLinea(pos1,pos2)
		for i in range(21):
			self.goal[0]=int(np.interp(q1[i]+150[0,300],[0,1022]))
			self.goal[1]=int(np.interp(q2[i]+150,[0,300],[0,1022]))
			self.goal[2]=int(np.interp(q3[i]+150,[0,300],[0,1022]))
			self.goal[3]=int(np.interp(q4[i]+150,[0,300],[0,1022]))
			self.jointCommand('',1,'Goal_Position',self.goal[0], 0.5)
			self.jointCommand('',2,'Goal_Position',self.goal[1], 0.5)
			self.jointCommand('',3,'Goal_Position',self.goal[2], 0.5)
			self.jointCommand('',4,'Goal_Position',self.goal[3], 0.5)
			self.rate.sleep()
		

	def equation(x,y,z):
		q1=np.arctan2(y,x)
		a=np.sqrt(x**2+y**2)
		alp=np.arctan2(z-136,a)
		b=np.sqrt((z-136)**2+a**2)
		q3s=np.sqrt(1-((b**2-2*(106**2))/(2*(106**2)))**2)
		q3c=(b**2-2*(106**2))/(2*(106**2))
		q3=np.arctan2(q3s,q3c)
		bets=(106*np.sin(q3+np.pi))/b
		betc=np.sqrt(1-((106*np.sin(q3+np.pi))/b)**2)
		bet=np.arctan2(bets,betc)
		q2=alp+bet-np.pi/2
		rotc=((1.0*(-1.0*np.sin(q1)*np.sin(q2 + 1.5707963267949))*np.sin(q3) + (1.0*np.sin(q1)*np.cos(q2 + 1.5707963267949))*np.cos(q3)))/\
		(1.0*(1.0*(-1.0*np.sin(q1)*np.sin(q2 + 1.5707963267949))*np.cos(q3) - (1.0*np.sin(q1)*np.cos(q2 + 1.5707963267949))*np.sin(q3)))
		rots=1/(1.0*(-1.0*np.sin(q3)*np.sin(q2 + 1.5707963267949) + 1.0*np.cos(q3)*np.cos(q2 + 1.5707963267949))*rotc - \
		(1.0*np.sin(q3)*np.cos(q2 + 1.5707963267949) + 1.0*np.sin(q2 + 1.5707963267949)*np.cos(q3)))
		rotc=rotc*rots
		q4=np.arctan2(rots,rotc)
		return (q1,q2,q3,q4)

	def linea(p1,p2):
		x=np.zeros([1,21])
		y=np.zeros([1,21])
		z=np.zeros([1,21])
		vn=np.linalg.norm(p2-p1)
		for i in range(21):
			x[0,i]=p1[0]+((i*vn)/20)*((p2[0]-p1[0])/vn)
			y[0,i]=p1[1]+((i*vn)/20)*((p2[1]-p1[1])/vn)
			z[0,i]=p1[2]+((i*vn)/20)*((p2[2]-p1[2])/vn)
		return x,y,z

	def makeLinea(p1,p2):
		x,y,z=linea(p1,p2)
		q1=np.empty((1,21))
		q2=np.empty((1,21))
		q3=np.empty((1,21))
		q4=np.empty((1,21))
		for i in range(21):
			q1[0,i],q2[0,i],q3[0,i],q4[0,i]=equation(x[0,i],y[0,i],z[0,i])
			print(z[0,i])
			if(q1[0,1]<0.01):
				q1[0,1]=0
			if(q2[0,1]<0.01):
				q2[0,1]=0
			if(q3[0,1]<0.01):
				q3[0,1]=0
			if(q4[0,1]<0.01):
				q4[0,1]=0
			#move goal
		return q1,q2,q3,q4

if __name__== "__main__": 
	try:
		temp=Moving()
	except: 
		rospy.loginfo("End of the trip for Robotica 2023-2") 