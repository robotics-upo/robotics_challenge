#!/usr/bin/env python

# A very basic TurtleBot script that moves TurtleBot forward indefinitely. Press CTRL + C to stop.  To run:
# On TurtleBot:
# roslaunch turtlebot_bringup minimal.launch
# On work station:
# python goforward.py

import sys
import math
import rospy
import tf
import numpy as np
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PointStamped
from sensor_msgs.msg import LaserScan

class Metrics:
    def __init__(self):
       
        self.listener = tf.TransformListener()
        
        self.goal_reached = False
    
        if not(rospy.has_param('~goal')):
            rospy.logfatal("You must specify the goal to this module via parameter server")
            
        self.base_frame = rospy.get_param('~base_frame', default='base_link')
        self.global_frame = rospy.get_param('~global_frame', default='map')
        
        self.output_file = rospy.get_param('~output_file', default='metrics.txt')
            
        self.goal_x = rospy.get_param('~goal/x', default=5)
        self.goal_y = rospy.get_param('~goal/y', default=5)  
        
        self.goal_gap = 0.25  # We will allow a 25 cm deviation from the goal
        
        self.has_transform = False
        
        while not(self.has_transform):
            self.init_x, self.init_y = self.getTransform()
            self.px = self.init_x
            self.py = self.init_y
        
        rospy.loginfo("Metrics: got transform! init_x = %f \tinit_y=%f", self.init_x, self.init_y)

        self.distance = 0
        self.init_time = rospy.Time.now()
        self.elapsed_time = -1.0

        self.historic_min_range = []
        self.historic_cmd_vel_lin = []
        self.historic_cmd_vel_ang = []
        
        self.max_lin = rospy.get_param('~max_lin', default=0.5)
        self.max_ang = rospy.get_param('~max_ang', default=1.0)
        self.ang_penalty = False
        self.lin_penalty = False  
        


        rospy.Subscriber("/scan", LaserScan, self.callback)
        rospy.Subscriber("/cmd_vel", Twist, self.cmd_vel_callback)

    def callback(self, data):
        self.historic_min_range.append(min(data.ranges))

    def cmd_vel_callback(self, data):
        self.historic_cmd_vel_lin.append(data.linear.x)
        self.historic_cmd_vel_ang.append(data.angular.z)
        if np.abs(data.linear.x) > self.max_lin:
            self.lin_penalty = True
        if np.abs(data.linear.x) > self.max_ang:
            self.ang_penalty = True

    def getTransform(self):
        try:
            (t,r) = self.listener.lookupTransform('map','base_link', rospy.Time(0))
            self.has_transform = True
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            return (0,0)

        return (t[0], t[1])
        
    def update(self):
        if self.goal_reached:
            return
        
        # rospy.loginfo("Metrics node. Acquiring new data")
        px,py = self.getTransform()
        self.distance += math.sqrt( (px-self.px)**2 + (py-self.py)**2)

        #Check for the goal:
        dist_goal = math.sqrt( (px-self.goal_x)**2 + (py-self.goal_y)**2)
        rospy.loginfo("Metrics update: Traveled distance %f. Distance to goal: %f", self.distance,dist_goal)

        self.px = px
        self.py = py
        
        if dist_goal < self.goal_gap:
            aux = rospy.Time.now() - self.init_time
            self.elapsed_time = float(aux.secs+aux.nsecs*1e-9)
            rospy.loginfo("Goal time. Elapsed time: %f", self.elapsed_time)
            self.goal_reached = True

    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stopped Metrics node. Generating statistics")
        (px, py) = self.getTransform()
        try:
            with open(self.output_file,'w') as f:
                f.write('Elapsed time: %f\n'%(float(self.elapsed_time)))
                f.write('Traveled Distance: %f\n'%(self.distance))
                if (len(self.historic_min_range) > 0):
                    f.write('Min distance to obstacles: %f\n'%(min(self.historic_min_range)))
                    f.write('Historic range: ')
                    f.write(' '.join(str(a) for a in self.historic_min_range))
                    f.write('\n')
                if (len(self.historic_cmd_vel_lin) > 0):
                    f.write('Linear penalty: %d\n'%(self.lin_penalty))
                    f.write('Historic linear cmd_vel: ')
                    f.write(' '.join(str(a) for a in self.historic_cmd_vel_lin))
                    f.write('\n')
                if (len(self.historic_cmd_vel_ang) > 0):
                    f.write('Angular penalty: %d\n'%(self.ang_penalty))
                    f.write('Historic angular cmd_vel: ')
                    f.write(' '.join(str(a) for a in self.historic_cmd_vel_ang))
                    f.write('\n')
                   
            rospy.loginfo('File exported successfully. Filename: %s', self.output_file)
        except OSError as e:
            rospy.logerr('Could not save output file. Filename = %s', str(e))
 
if __name__ == '__main__':
    try:
	    # initiliaze
        rospy.init_node('Metrics', anonymous=False)

	    # tell user how to stop TurtleBot
        rospy.loginfo("To stop the Metrics node press CTRL + C")

        metrics=Metrics()
	    # What function to call when you ctrl + c    
        rospy.on_shutdown(metrics.shutdown)

        #TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
        r = rospy.Rate(10)

        # as long as you haven't ctrl + c keeping doing...
        while not rospy.is_shutdown():
            # publish the velocity
            metrics.update()
            # wait for 0.1 seconds (10 HZ) and publish again
            r.sleep()
    except:
        rospy.loginfo("Metrics node terminated.")
