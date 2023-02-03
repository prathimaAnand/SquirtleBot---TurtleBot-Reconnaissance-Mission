#!/bin/bash

echo "Launching ROS: $(hostname -s).launch"

# This sets up the environment correctly
export PYTHONPATH=
. /home/ubuntu/squirtle_workspace/devel/setup.bash

# Set the log file directory to something sane.
DATETIME=`date '+%Y-%m-%d_%H-%M-%S'`
DIRNAME=/home/robot/data/ros_log/$DATETIME
mkdir -p $DIRNAME
export ROS_LOG_DIR=$DIRNAME
rm /home/ubuntu/data/ros_log/latest
ln -sf $DIRNAME/latest /home/ubuntu/data/ros_log/latest

# Use roslaunch with the launch file for this vehicle
/opt/ros/noetic/bin/roslaunch /home/ubuntu/squirtle_workspace/src/launch/$(hostname -s).launch
