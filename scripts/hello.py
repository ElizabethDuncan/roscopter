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

def dearm():
	print "in dearm"
	rospy.wait_for_service('command')
	try:
		command = rospy.ServiceProxy('command', roscopter.srv.APMCommand)
		res = command(4)
		if str(res) == "result: True":
			print "successfully dearming"
			return True
		else:
			print "error dearming"
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
		command = rospy.ServiceProxy('command', roscopter.srv.APMCommand)
		res = command(2)
		if str(res) == "result: True":
			print "successfully landing"
			return True
		else:
			print "error landing"
			return False
	except rospy.ServiceException, e:
		return False

def send_waypoint():
	print "in send waypoint"
	rospy.wait_for_service('waypoint')
	try:
		send_waypoint_command = rospy.ServiceProxy('waypoint', roscopter.srv.SendWaypoint)
		waypoint1 = {latitude: 42.2914092, longitude: -71.2624439, altitude: 5000, 
					 pos_acc: 10, speed_to: 10, hold_time: 10, yaw_from: 10, 
					 pan_angle: 10, tilt_angle: 10, waypoint_type: 1}		
		res = send_waypoint_command(waypoint1)
		if str(res) == "result: True":
			print "successfully sent waypoint"
			return True
		else:
			#Try one more time to send waypoint
			res = command(waypoint1)
			if str(res) == "result: True":
				print "successfully sent waypoint"
				return True
			else:
				print "error sending waypoint"
				return False
	except rospy.ServiceException, e:
		return False



def gps_received(data):
	print "gps data: " + str(data)

def get_gps():
	rospy.wait_for_topic('gps')
	try:
		rospy.Subscriber("gps", TODO, gps_received)
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


if __name__ == "__main__":
	if goto_waypoint():
		print "mission successfull"
	else:
		return_control()
		print "mission failure"
		
