#!/usr/bin/env python

import rospy
import roscopter.msg
import time

global flag  

# rostopic pub -1 /send_rc roscopter/RC '{channel: [0,0,0,0,0,1050,1530,0]}'


def main():
    global flag

    pub = rospy.Publisher('/send_rc', roscopter.msg.RC, queue_size=10)
    sub = rospy.Subscriber('/send_rc',roscopter.msg.RC, checker)
    rospy.init_node("gimbal_init", anonymous=True)

    flag = False
    i = 0
    while not flag and i<5:
        i+=1
        pub.publish([0,0,0,0,0,1050,0,0])
        time.sleep(1)
        print flag

def checker(data):
    global flag
    flag = True


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        print "derp"