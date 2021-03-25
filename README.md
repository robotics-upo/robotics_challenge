# robotics_challenge
Robotic challenge scenarios for the Robotics and Advanced subject of UPO's Software Engineering Grade

## Installation instructions

This branch has been specifically adapted to the ROS Melodic distribution, and tested in Ubuntu 18.04.

We provide you with a useful installation script that you can use for easily installing it into a ROS workspace. To use it you have to specify the target catkin workspace where the node should be installed. To do this you can use:

```
rosrun robotics_challenge install.bash
```

## How to use the challenge

The goal of the challenge is to setup the simulation environment in which your path tracking, path planning and collision avoidance modules should be used in order to guide the Turtlebot robot to a goal destination.

This configuration includes the setup of:

* A gazebo world file that has the environment where the robot is placed on.
* The spawn of a Turtlebot robot equipped with a LASER sensor and a RGBD camera.
* The localization module (AMCL) and the map that should be used as the frame to determine the navigation goals.

A convenient bash script is available for each scenario (1-3). Example:

```
$  rosrun robotics_challenge robotics_challenge_1.bash
```
