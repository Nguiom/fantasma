#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from tkinter import *
from tkinter import ttk
import numpy as np

class interface:
    def __init__(self,root):

        rospy.init_node('State', anonymous=False)
        self.key_sub= rospy.Subscriber("/dynamixel_workbench/joint_states",JointState, self.read)
        rate=rospy.Rate(0.5)
        self.state=1
        root.title("Lineal")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        self.z=0
        self.zOff = StringVar()
        feet_entry = ttk.Entry(mainframe, width=7, textvariable=self.feet)
        feet_entry.grid(column=4, row=1, sticky=(W, E))
        ttk.Label(mainframe, text="Offset").grid(column=1, row=1, sticky=(W, E))
        ttk.Button(mainframe, text="Save", command=self.offset).grid(column=5, row=1, sticky=W)

        self.xC=StringVar()
        self.yC=StringVar()
        self.zC=StringVar()
        ttk.Label(mainframe, text="Current").grid(column=1, row=2, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.xC).grid(column=2, row=2, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.yC).grid(column=3, row=2, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.zC).grid(column=4, row=2, sticky=(W, E))
        ttk.Button(mainframe, text="On/off", command=self.on).grid(column=5, row=2, sticky=W)

        ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
        ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
        ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        feet_entry.focus()
        root.bind("<Return>", self.calculate)

    def offset(self, *args):
        try:
            self.z = float(self.zOff.get())
        except ValueError:
            pass

    def on(self,command, id_num, addr_name, value, time):
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
    
    def read(self,data):
        pass

if __name__== "__main__": 
        root = Tk()
        interface(root)
        root.mainloop()
