#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Header, Bool
from std_srvs.srv import *
from sensor_msgs.msg import NavSatFix, NavSatStatus, Imu
import roscopter.msg
import roscopter.srv
import sys,struct,time,os
import math
import driver


##******************************************************************************
 # Name:    start_mission
 # Purpose: Callback function for "mission" Service.  Specific commands are used
 #              to control functions such as Start mission, finish mission and 
 #				failsafe.
 #              All commands may be found within the "XCEECommand" Service file.
 #              New commands should be entered there to keep uniform constants
 #              throughout calling functions
 # Params:  data: Requested command variable
#*******************************************************************************
def start_mission(req):
	print req
	driver.goto_waypoint()

def land_it(req):
	if req.command == roscopter.srv.XBEECommand.STARTMISSION:
		driver.land()	


##******************************************************************************
# Services for APM Commands
#*******************************************************************************
# Allow for commands such as Arm, Disarm, Launch, Land, etc.
rospy.Service("mission", roscopter.srv.APMCommand, start_mission)
rospy.Service("land", roscopter.srv.XBEECommand, land_it)


if __name__ == '__main__':
    try:
        # initially clear waypoints and start mainloop
        driver.clear_waypoints()
#        if (opts.enable_ros_failsafe):
#            rospy.Timer(rospy.Duration(1), ros_failsafe_check)        
        driver.mainloop()
    except rospy.ROSInterruptException: pass