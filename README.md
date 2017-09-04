# swarm-robotics
This project is about swarm robotics with ros.
Main task is rescueing people from natural disasters or rescueing lost people.. 
In this project ros is used to control robots, gazebo is used for simulating scenario and hog feature for detecting people with camera. 
To use this project you need to install ubuntu 14.04 or Linux Mint 17.1, ROS Indigo Distribution, Gazebo 2.2 and Hector Quadrotor Packages.
You can use modeldownload.sh to install gazebo models, which is copied from http://machineawakening.blogspot.com.tr/2015/05/how-to-download-all-gazebo-models.html .
Project needs a walking human model which is named actor but hector quadrotor packages don't run properly in Gazebo 8.
Gazebo 2.2 has no actor also, so you need to change one of pioneers' chasis mesh from either xacro from the project or from gazebo's xacro file which is in the "gazebo_plugins/test/multi_robot_scenario".
And in this project we used an interval of angles which we choose to read laser values. But it can be calculated from Hog detection to detect where is the human. It is commented right before the line that we used the angle.
After installing all of the dependencies, project can be run with roslaunch command and using "demo.launch" file.
