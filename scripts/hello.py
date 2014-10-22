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
import ctypes
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

def waypoint_test():
    print "in waypoint_test"
    rospy.wait_for_service('waypoint_test')
    try:
        command = rospy.ServiceProxy('waypoint_test', Empty)
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
    new_wp.latitude = int((current_gps.latitude - 0.00002) * 1e+7)
    new_wp.longitude = int((current_gps.longitude - 0.00002) * 1e+7)
    print "raw_alt", current_gps.altitude
    new_wp.altitude = current_gps.altitude*100
    new_wp.hold_time = (1 * 10000)
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

# Only works for Empty type services
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

def call_service(service_name):
    rospy.loginfo("call service calling" + str(service_name))
    rospy.wait_for_service(str(service_name))
    try:
        print "trying to start " + str(service_name)
        mission = rospy.ServiceProxy(str(service_name), Empty)
        res = mission()
        print "sent command to " + str(service_name)
    except rospy.ServiceException, e:
        print "Error: ", e
        return False

import time


if __name__ == "__main__":
    rospy.init_node("hello")

    new_wp = roscopter.msg.Waypoint()
    new_wp.latitude = int(42.2926834 * 1e+7)
    new_wp.longitude = int(-71.2628237 * 1e+7)
    new_wp.altitude = 5000
    new_wp.hold_time = (3 * 1000)
    new_wp.waypoint_type = roscopter.msg.Waypoint.TYPE_NAV
    new_wp2 = roscopter.msg.Waypoint()
    new_wp2.latitude = int(42.2925417 * 1e+7)
    new_wp2.longitude = int(-71.2628411 * 1e+7)
    new_wp2.altitude = 5000
    new_wp2.hold_time = (3 * 1000)
    new_wp2.waypoint_type = roscopter.msg.Waypoint.TYPE_NAV

    if arm() and launch() and send_waypoint(new_wp):
        call_service("trigger_auto")
        # call_service("adjust_throttle")
        # start_mission()
        time.sleep(15)
        send_waypoint(new_wp2)
        time.sleep(15)
        land()
    else:
        print "mission failure"
        
