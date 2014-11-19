uint8 coordinate_frame
uint8 FRAME_LOCAL_NED = 1
uint8 FRAME_LOCAL_OFFSET_NED = 7
uint8 FRAME_BODY_NED = 8
uint8 FRAME_BODY_OFFSET_NED = 9

uint16 type_mask

uint8 MASK_USE_ALL = 0
uint8 MASK_IGNORE_X = 1
uint8 MASK_IGNORE_Y = 2
uint8 MASK_IGNORE_Z = 4
uint8 MASK_IGNORE_VX = 8
uint8 MASK_IGNORE_VY = 16
uint8 MASK_IGNORE_VZ = 32
uint8 MASK_IGNORE_AX = 8
uint8 MASK_IGNORE_AY = 16
uint8 MASK_IGNORE_AZ = 32
uint8 MASK_FORCE = 64
uint8 MASK_IGNORE_YAW = 128
uint8 MASK_IGNORE_YAW_RATE = 256

float32 x
float32 y
float32 z
float32 vx
float32 vy
float32 vz
float32 ax
float32 ay
float32 az
float32 yaw
float32 yaw_rate
