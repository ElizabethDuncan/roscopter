# latitude and longitude given in decimal degrees (* 10^7)
int32 latitude
int32 longitude

# height in mm
int32 altitude

# posAcc given in mm
uint16 pos_acc

# max speed to travel to waypoint in % of 100
uint8 speed_to

# time to stay at waypoint in ms
uint16 hold_time

# yawFrom angle given in degrees (* 1000)
int32 yaw_from

# camera pan and tilt angles during waypoint travel given in degrees (* 1000)
int32 pan_angle
int32 tilt_angle

# Type of Waypoint
uint8 waypoint_type

# Coordinate frame to use
uint8 waypoint_frame

uint8 TYPE_NAV = 1
uint8 TYPE_CONDITION_YAW = 2
uint8 TYPE_CONDITION_CHANGE_ALT = 3
uint8 TYPE_TAKEOFF = 4

uint8 MAV_FRAME_GLOBAL = 0
uint8 MAV_FRAME_LOCAL_NED = 1
uint8 MAV_FRAME_MISSION = 2
uint8 MAV_FRAME_GLOBAL_RELATIVE_ALT = 3
uint8 MAV_FRAME_LOCAL_ENU = 4
uint8 MAV_FRAME_LOCAL_OFFSET_NED = 7
uint8 MAV_FRAME_BODY_NED = 8
uint8 MAV_FRAME_BODY_OFFSET_NED = 9
uint8 MAV_FRAME_GLOBAL_TERRAIN_ALT = 10
