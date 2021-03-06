Installation Instructions
=======================

Clone or fork this repo!

`git clone https://github.com/ElizabethDuncan/roscopter.git`  

Navigate to repo folder (called 'roscopter')

`cd roscopter/scripts`  

Navigate to the scripts folder and run command:

`chmod 777 driver.py`  

Navigate back to repo folder

`cd ..`  

Checkout mavlink using submodule. 

`git submodule init`  
`git submodule update`

Build mavlink.

`cd mavlink/pymavlink`  
`sudo python setup.py install`  

Navigate back to Catkin folder and run 'catkin_make'.  

`cd ~/catkin_ws/`  
`catkin_make`  

Add your user to the dialout group to have access to the USB radio. This may require reboot to take effect.

`sudo adduser $USER dialout`  

Note
=======================
Use in conjuction with https://github.com/hboortz/arl-scope for autonomous quadcopter control/missions.

Background
=======================

Roscopter code used for ARL SCOPE Project 2014, video streaming quadcopters

Forked from https://github.com/epsilonorion/roscopter

Team members: Elizabeth Duncan, Kyle McConnaughay, Eric Schneider, Charles Goddard, Heather Boortz, and Katilin Gallagher

