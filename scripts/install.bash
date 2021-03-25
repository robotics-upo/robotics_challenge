#! /bin/bash
# Note: Use this script as a regular user. It will request sudo on demand

if [[ $ROS_DISTRO. -eq . ]]
then
    echo "Please configure ROS before using this script. Try with: 'source/opt/ros/<your ROS distro>/setup.bash'"
    exit -1
fi

## Install yocs stuff
A=ros-$ROS_DISTRO
P=${A}-yocs-
sudo apt install ${P}ar-marker-tracking ${P}ar-pair-approach ${P}ar-pair-tracking ${P}cmd-vel-mux ${P}controllers \
${P}joyop ${P}keyop ${P}localization-manager ${P}math-toolkit ${P}msgs ${P}navi-toolkit ${P}navigator ${P}rapps ${P}safety-controller ${P}velocity-smoother ${P}virtual-sensor ${P}waypoint-provider ${P}waypoints-navi -y

# Install ROS dependencies
sudo apt install $A-base-local-planner $A-turtlebot3-gazebo $A-amcl $A-map-server -y

# Additional utils
sudo apt install pyqt5-dev-tools $A-ecl-core $A-ecl-mobile-robot libusb-dev libftdi-dev -y


# Compile the stuff
cd ..
catkin_make
