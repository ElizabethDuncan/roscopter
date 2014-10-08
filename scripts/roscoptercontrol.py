#!/usr/bin/env python
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


##******************************************************************************
# Services for APM Commands
#*******************************************************************************
# Allow for commands such as Arm, Disarm, Launch, Land, etc.
rospy.Service("mission", roscopter.srv.XBEECommand, start_mission)


if __name__ == '__main__':
    try:
        # initially clear waypoints and start mainloop
        driver.clear_waypoints()
#        if (opts.enable_ros_failsafe):
#            rospy.Timer(rospy.Duration(1), ros_failsafe_check)        
        driver.mainloop()
    except rospy.ROSInterruptException: pass