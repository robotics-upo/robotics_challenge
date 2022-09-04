#! /bin/bash
export y=0.3
roslaunch robotics_challenge robotics_challenge.launch scenario:=house init_y:=$y initial_pose_y:=$y map_name:=house_reduced.yaml goal_x:=1.1 goal_y:=1.5
