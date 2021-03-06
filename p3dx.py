#!/usr/bin/env python
# -*- coding: utf-8 -*-

import roslib
import rospy
import sys
import math
import tf as tf

from time import sleep
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from math import radians

class Robot():
    def __init__(self, name):
        self.pose = None
        self.orient = None
        self.euler = None
        self.name = name
        self.odom = rospy.Subscriber("/" + name + "/odom", Odometry, self.odom_callback)
        self.cmd  = rospy.Publisher("/" + name + '/cmd_vel', Twist, queue_size=10)
        self.twist = Twist()
        self.rate = rospy.Rate(10)
    
    def odom_callback(self, data):
        position = data.pose.pose.position
        orientation = data.pose.pose.orientation
        self.pose = position
        self.pose.y = self.pose.y
        self.orient = (
            orientation.x,
            orientation.y,
            orientation.z,
            orientation.w,
            )
        self.euler = tf.transformations.euler_from_quaternion(self.orient)
        
    def rotate_robot(self, yawangle):
        eu = self.euler[2]
        zero = yawangle - eu
        multiplier = 1.0
        if zero > 0:
            multiplier = 1.0
            if zero > 3.1:
                multiplier = -1.0
        else:
            multiplier = -1.0

        self.twist.linear.x = 0.0   
        self.cmd.publish(self.twist)
        while not (eu < (yawangle + math.radians(5)) and  eu > (yawangle - math.radians(5))):
            if (abs(eu - yawangle)) > math.radians(15):
                self.twist.angular.z = math.radians(15) * multiplier
                self.cmd.publish(self.twist)
            elif abs(eu - yawangle) > math.radians(5):
                self.twist.angular.z = math.radians(2) * multiplier
                self.cmd.publish(self.twist)
            else:
                self.twist.angular.z = math.radians(1) * multiplier
                self.cmd.publish(self.twist)
                
            eu = self.euler[2]
            
        self.twist.angular.z = 0
        self.cmd.publish(self.twist)
        
    def rotate_robot_2(self, yawangle):
        eu = self.euler[2]
        zero = yawangle - eu
        multiplier = 1.0
        if zero > 0:
            multiplier = 1.0
            if zero > 3.1:
                multiplier = -1.0
        else:
            multiplier = -1.0

        if (eu < (yawangle + math.radians(5)) and  eu > (yawangle - math.radians(5))):
            return
        elif (abs(eu - yawangle)) > math.radians(15):
            self.twist.angular.z = math.radians(15) * multiplier
        elif abs(eu - yawangle) > math.radians(5):
            self.twist.angular.z = math.radians(2) * multiplier
        else:
            self.twist.angular.z = math.radians(1) * multiplier
            
    def goto_point(self, px, py, pz):
        completed = False

        while not completed:
            if self.pose != None:
                x = self.pose.x
                y = self.pose.y
                eu = self.euler[2]
                dist = ((px - x) ** 2 + (py - y) ** 2) ** 0.5
                angle = math.atan2(py - y, px - x)
    
                radius = dist * 0.5 / math.sin(eu - angle) if eu - angle != 0.0 else float('Inf')
    
                linear = angular = 0.0
                
                fx = px - x
                fy = py - y 
                
                field = return_field(fx, fy)

                if (field == 1):
                    yawangle = math.asin(fy/dist)
                    self.rotate_robot_2(yawangle)
                    
                elif (field == 2):
                    yawangle = math.radians(180) - math.asin(fy/dist)
                    self.rotate_robot_2(yawangle)

                elif (field == 3):
                    yawangle = math.radians(180) - math.asin(fy/dist)
                    yawangle *= -1.0
                    self.rotate_robot_2(yawangle)

                elif (field == 4):
                    yawangle = math.asin(fy/dist)
                    self.rotate_robot_2(yawangle)

                elif (field == 5):
                    yawangle = math.asin(fy/dist)
                    if yawangle > math.radians(180):
                        yawangle *= -1.0
                    self.rotate_robot_2(yawangle)

                if dist > 5:
                    self.twist.linear.x = 0.8   
                    self.cmd.publish(self.twist)
                elif dist > 0.20:
                    self.twist.linear.x = 0.1
                    self.cmd.publish(self.twist)
                else:
                    completed = True
                                    
                self.rate.sleep()
            else:
                pass

    def control_help(self):
            while(True):
                try:
                    fo = open("/home/yigit/catkin_ws/src/quadro_demo/src/swarm-robotics/communication/goto_points.txt", "r")
                    filestring = fo.readline()
                    if (filestring != None):
                        px, py, pz = filestring.split()
                        self.goto_point(float(px), float(py), float(pz))
                    fo.close()
                except:
                    pass
        
def return_field(x, y):
    if (x > 0 and y > 0):
        return 1
    elif (x < 0 and y > 0):
        return 2
    elif (x < 0 and y < 0):
        return 3
    elif (x > 0 and y < 0):
        return 4
    else: 
        return 5
    
def main(name):    
    rospy.init_node('P3dx', name)
    robot = Robot(name)
    robot.control_help()

if __name__ == '__main__':
    main(sys.argv[1])