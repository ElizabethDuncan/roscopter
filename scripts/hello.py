#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Header, Bool
from std_srvs.srv import *
from sensor_msgs.msg import NavSatFix, NavSatStatus, Imu
import roscopter.msg
import roscopter.srv
import sys,struct,time,os
import math
import xmlrpclib
#import driver


def arm():
    rospy.loginfo("in arm")
    rospy.wait_for_service('command')
    try:
        print "trying to arm"
        command = rospy.ServiceProxy('command', roscopter.srv.APMCommand)
        res = command(3)
        print 'res:', res
        if str(res) == "result: True":
            print "successfully armed"
            return True
        else:
            print "error arming"
            return False
    except rospy.ServiceException, e:
        print "Error: ", e
        return False

# TODO look at the launch code - how high is it going to go
def launch():
    print "in launch"
    rospy.wait_for_service('command')
    try:
        command = rospy.ServiceProxy('command', roscopter.srv.APMCommand)
        res = command(1)
        print 'res:', res
        if str(res) == "result: True":
            print "successfully launching"
            return True
        else:
            print "error launching"
            return False
    except rospy.ServiceException, e:
        print "Error: ", e
        return False

def land():
    print "in land"
    rospy.wait_for_service('command')
    try:
    	print "sending land command"
        command = rospy.ServiceProxy('land', Empty)
        res = command()
        print 'res:', res
        if str(res) == "result: True":
            print "successfully landing"
            return True
        else:
            print "error landing"
            return False
    except rospy.ServiceException, e:
        print "Error: ", e
        return False

def land_failsafe():
    print "in land_failsafe"
    rospy.wait_for_service('command')
    try:
        command = rospy.ServiceProxy('land_failsafe', Empty)
        res = command()
        print 'res:', res
        if str(res) == "result: True":
            print "successfully landing"
            return True
        else:
            print "error landing"
            return False
    except rospy.ServiceException, e:
        print "Error: ", e
        return False


def send_waypoint(wp):
    print "in send waypoint"
    rospy.wait_for_service('waypoint')
    try:
        send_waypoint_command = rospy.ServiceProxy('waypoint', roscopter.srv.SendWaypoint)
        res = send_waypoint_command(wp)
        print 'res:', res
        if str(res) == "result: True":
            print "successfully sent waypoint"
            return True
        else:
            #Try one more time to send waypoint
            res = send_waypoint_command(wp)
            if str(res) == "result: True":
                print "successfully sent waypoint"
                return True
            else:
                print "error sending waypoint"
                return False
    except rospy.ServiceException, e:
        print "Error: ", e
        return False


current_gps = None
target_wp = None


def use_gps_to_set_waypoint():
    # Create new  Waypoint
    new_wp = roscopter.msg.Waypoint()
    #increment latitiude by just a little
    new_wp.latitude = (current_gps.latitude - 0.00002) * 1e+7
    new_wp.longitude = (current_gps.longitude - 0.00002) * 1e+7
    new_wp.altitude = 6000
    new_wp.waypoint_type = roscopter.msg.Waypoint.TYPE_NAV

    global target_wp
    target_wp = new_wp
    send_waypoint(new_wp)

def gps_received(data):
    global current_gps
    current_gps = data

def get_gps():
    rospy.wait_for_message('gps', NavSatFix)
    try:
        message = rospy.Subscriber("gps", NavSatFix, gps_received)
        return message
    except rospy.ServiceException, e:
        print "Error: ", e
        return False


def return_control():
    print "in return_control"
    rospy.wait_for_service('command')
    try:
        command = rospy.ServiceProxy('command', roscopter.srv.APMCommand)
        res = command(10)
        print 'res:', res
        if str(res) == "result: True":
            print "successfully returning control"
            return True
        else:
            print "error returning control"
            return False
    except rospy.ServiceException, e:
        print "Error: ", e
        return False


def start_mission():
    rospy.loginfo("in start mission")
    rospy.wait_for_service('mission')
    try:
        print "trying to start mission"
        mission = rospy.ServiceProxy('mission', roscopter.srv.APMCommand)
        res = mission(1)
        print 'res:', res
        if str(res) == "result: True":
            print "successfully started mission"
            return True
        else:
            print "error starting mission"
            return False
    except rospy.ServiceException, e:
        print "Error: ", e
        return False


if __name__ == "__main__":

    #wp = Waypoint(42.2926476, -71.2629756, 5000, 10, 10, 10, 10, 10, 10, 1)
    rospy.init_node("hello")
    if arm() and get_gps() and launch():
        print "Starting wait 0/30"
        rospy.sleep(10)

        use_gps_to_set_waypoint()

        print "At wait 10/30"
        rospy.sleep(10)
        print "At wait 20/30"
        rospy.sleep(10)
        print "Landing"
        rospy.sleep(1)
        if land():
            print "mission successfull"
    else:
        print "mission failure"
        
