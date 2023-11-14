#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from std_msgs.msg import Int32MultiArray
from tkinter import *
from tkinter import ttk
import numpy as np
from dynamixel_workbench_msgs.srv import DynamixelCommand

class interface:
    def __init__(self,root):

        self.state=0
        root.title("Lineal")
        self.goals={}

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        self.z=0
        self.zOff = StringVar()
        self.zOff.set(136)
        feet_entry = ttk.Entry(mainframe, width=7, textvariable=self.zOff)
        feet_entry.grid(column=3, row=1, sticky=(W, E))
        ttk.Label(mainframe, text="Offset").grid(column=1, row=1, sticky=(W, E))
        ttk.Button(mainframe, text="Save", command=self.offset()).grid(column=5, row=1, sticky=W)
        ttk.Button(mainframe, text="Grab", command=self.grab()).grid(column=4, row=1, sticky=W)

        self.xC=StringVar()
        self.yC=StringVar()
        self.zC=StringVar()
        ttk.Label(mainframe, text="Current").grid(column=1, row=2, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.xC).grid(column=2, row=2, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.yC).grid(column=3, row=2, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.zC).grid(column=4, row=2, sticky=(W, E))
        ttk.Button(mainframe, text="On/off", command=self.on()).grid(column=5, row=2, sticky=W)

        self.xG=StringVar()
        self.xG.set(100)
        self.yG=StringVar()
        self.yG.set(100)
        self.name=StringVar()
        self.name.set("p1")
        self.nameList=[]
        ttk.Label(mainframe, text="Goal").grid(column=1, row=3, sticky=(W, E))
        xG_entry = ttk.Entry(mainframe, width=7, textvariable=self.xG)
        xG_entry.grid(column=2, row=3, sticky=(W, E))
        yG_entry = ttk.Entry(mainframe, width=7, textvariable=self.yG)
        yG_entry.grid(column=3, row=3, sticky=(W, E))
        name_entry = ttk.Entry(mainframe, width=7, textvariable=self.name)
        name_entry.grid(column=4, row=3, sticky=(W, E))
        ttk.Button(mainframe, text="Save", command=self.newGoal()).grid(column=5, row=3, sticky=W)

        self.p1=StringVar()
        self.p2=StringVar()
        self.p1_entry=ttk.Combobox(mainframe, textvariable=self.p1,postcommand=self.updateP1)
        self.p1_entry.grid(column=1, row=4, sticky=(W, E))
        self.p2_entry=ttk.Combobox(mainframe, textvariable=self.p1,postcommand=self.updateP2)
        self.p2_entry.grid(column=3, row=4, sticky=(W, E))
        ttk.Button(mainframe, text="Go", command=self.go()).grid(column=5, row=5, sticky=W)

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        rospy.init_node('State', anonymous=False)
        self.key_sub= rospy.Subscriber("/dynamixel_workbench/joint_states",JointState, self.read)
        self.move =rospy.Publisher('move',Int32MultiArray, queue_size=10)
        rate=rospy.Rate(0.5)

    def offset(self, *args):
        try:
            self.z = int(self.zOff.get())
        except ValueError:
            pass

    def on(self):
        rospy.wait_for_service('dynamixel_workbench/dynamixel_command')
        try:
            dynamixel_command = rospy.ServiceProxy(
                '/dynamixel_workbench/dynamixel_command', DynamixelCommand)
            dynamixel_command('',1,'Torque_Enable',self.state)
            dynamixel_command('',2,'Torque_Enable',self.state)
            dynamixel_command('',3,'Torque_Enable',self.state)
            dynamixel_command('',4,'Torque_Enable',self.state)
            dynamixel_command('',5,'Torque_Enable',self.state)
            if(self.state==1):
                self.state=0
            elif(self==0):
                self.state=1
        except rospy.ServiceException as exc:
            print(str(exc))

    def grab(self):
        rospy.wait_for_service('dynamixel_workbench/dynamixel_command')
        try:
            dynamixel_command = rospy.ServiceProxy(
                '/dynamixel_workbench/dynamixel_command', DynamixelCommand)
            dynamixel_command('',5,'Goal_Position',100)
        except rospy.ServiceException as exc:
            print(str(exc))

    def newGoal(self,*args):
        self.goals.update({self.name.get():[int(float(self.xG.get())),\
        int(self.yG.get()),self.z]})
        self.nameList.append(self.name.get())

    def updateP1(self,*args):
        self.p1_entry['values']=self.nameList

    def updateP2(self,*args):
        self.p2_entry['values']=self.nameList
    
    def go(self):
        temp1=self.p1.get()
        temp2=self.p2.get()
        temp1=self.goals.get(temp1,[100,1,136])
        temp2=self.goals.get(temp2,[100,1,136])
        self.move.publish(temp1+temp2)
    
    def read(self,data):
        pass

if __name__== "__main__": 
        root = Tk()
        interface(root)
        root.mainloop()