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
		print type(res), res
		if str(res) == "result: True":
			print "successfully armed"
			return True
		else:
			print "error arming"
			return False
	except rospy.ServiceException, e:
		return False

# TODO look at the launch code - how high is it going to go
def launch():
	print "in launch"
	rospy.wait_for_service('command')
	try:
		command = rospy.ServiceProxy('command', roscopter.srv.APMCommand)
		res = command(1)
		print res
		if str(res) == "result: True":
			print "successfully launching"
			return True
		else:
			print "error launching"
			return False
	except rospy.ServiceException, e:
		return False


def land():
	print "in land"
	rospy.wait_for_service('command')
	try:
		command = rospy.ServiceProxy('land', roscopter.srv.XBEECommand)
		res = command(1)
		if str(res) == "result: True":
			print "successfully landing"
			return True
		else:
			print "error landing"
			return False
	except rospy.ServiceException, e:
		return False

from collections import namedtuple
Waypoint = namedtuple('Waypoint', 'latitude longitude altitude pos_acc speed_to hold_time yaw_from pan_angle tilt_angle waypoint_type')


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
		return False


def use_gps_to_set_waypoint():
	gps = get_gps()
	# Create new  Waypoint
    new_wp = roscopter.msg.Waypoint()
    #increment latitiude by just a little
    new_wp.latitude = gps.latitude + 0.0001
    new_wp.longitude = gps.longitude
    new_wp.altitude = gps
    new_wp.waypoint_type = roscopter.msg.Waypoint.TYPE_NAV

    send_waypoint(new_wp)

def gps_received(data):
	return data

def get_gps():
	rospy.wait_for_topic('gps')
	try:
		message = rospy.Subscriber("gps", NavSatFix, gps_received)
		return message
	except rospy.ServiceException, e:
		return False


def return_control():
	print "in return_control"
	rospy.wait_for_service('command')
	try:
		command = rospy.ServiceProxy('command', roscopter.srv.APMCommand)
		res = command(10)
		if str(res) == "result: True":
			print "successfully returning control"
			return True
		else:
			print "error returning control"
			return False
	except rospy.ServiceException, e:
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
		return False


if __name__ == "__main__":

	wp = Waypoint(42.2914092, -71.2624439, 5000, 10, 10, 10, 10, 10, 10, 1)

	if arm() and launch() and use_gps_to_set_waypoint() and start_mission():
		print "mission successfull"
	else:
		return_control()
		print "mission failure"
		
