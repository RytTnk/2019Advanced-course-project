#! /usr/bin/env python
# -*- coding: utf-8 -*-

#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Include library -----
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
#_____________________________________________________________________


#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Utility of joy controller library -----
######################################################################
## @version    0.1.0
## @author     K.Ishimori
## @date       2019/10/12 Newly created.                  [K.Ishimori]
## @brief      Utility of joy library
######################################################################
class joy_con_utility:
    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Initialized utility class -----
    ######################################################################
    ## @brief      Initialized utility class
    ######################################################################
    def __init__(self):
        rospy.init_node('joy_con_node', anonymous=True)
        self.twist_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=1000)
        rospy.Subscriber('joy',Joy, self.joy_callback)

        self.twist = Twist()
        self.twist.linear.x = 0.0
        self.twist.linear.y = 0.0
        self.twist.linear.z = 0.0
        self.twist.angular.x = 0.0
        self.twist.angular.y = 0.0
        self.twist.angular.z = 0.0
        self.twist_pub.publish(self.twist)
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Joy controller callback -----
    ######################################################################
    ## @brief      Joy controller callback
    ## @param[in]  joy : joy controller data
    ######################################################################
    def joy_callback(self, joy):
        self.twist.linear.x  = joy.axes[1]
        self.twist.linear.y  = 0.0
        self.twist.angular.z = joy.axes[0]
        self.twist_pub.publish(self.twist)

        self.twist_debug()
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Twist data debug -----
    ######################################################################
    ## @brief      Twist data debug
    ######################################################################
    def twist_debug(self):
        x_str = str("{0:.2f}".format(self.twist.linear.x)).rjust(5)
        y_str = str("{0:.2f}".format(self.twist.linear.y)).rjust(5)
        z_str = str("{0:.2f}".format(self.twist.angular.z)).rjust(5)
        print x_str, y_str, z_str
    #_____________________________________________________________________


#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Main processing -----
######################################################################
## @brief      Main processing
## @callgraph
## @callergraph
######################################################################
if __name__ == '__main__':
    try:
        ts = joy_con_utility()
        rospy.spin()
    except rospy.ROSInterruptException: pass
