import time
import board
import math
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import (BNO_REPORT_ROTATION_VECTOR, BNO_REPORT_LINEAR_ACCELERATION)

# I2C initialization (address 0x4b)
i2c = board.I2C()
bno = BNO08X_I2C(i2c, address=0x4b)

# Enable rotation vector (fusion of accel, gyro, mag)
bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)
bno.enable_feature(BNO_REPORT_LINEAR_ACCELERATION)

def quaternion_to_euler(quat):
    """
    Converts quaternions (x, y, z, w) to Euler angles (roll, pitch, yaw)
    """
    x, y, z, w = quat

    # Roll (X-axis)
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    # Pitch (Y-axis)
    sinp = 2 * (w * y - z * x)
    if abs(sinp) >= 1:
        pitch = math.copysign(math.pi / 2, sinp) # clamped at 90 degrees
    else:
        pitch = math.asin(sinp)

    # Yaw (Z-axis / heading)
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    # Convert to degrees
    roll_deg = math.degrees(roll)
    pitch_deg = math.degrees(pitch)
    yaw_deg = math.degrees(yaw)

    # Normalize yaw to 0-360 degrees
    if yaw_deg < 0:
        yaw_deg += 360

    return roll_deg, pitch_deg, yaw_deg

print("BNO08x 3-axis measurement active...")


try:
    while True:
        quat = bno.quaternion
        
        if quat is not None:
            r, p, y = quaternion_to_euler(quat)
            lin_x, lin_y, lin_z = bno.linear_acceleration
            #print(f"LINEAR -> X: {lin_x:6.2f} Y: {lin_y:6.2f} Z: {lin_z:6.2f}")
            #print(f"X (Roll): {r:7.2f}° | Y (Pitch): {p:7.2f}° | Z (Yaw): {y:7.2f}°")
            
        time.sleep(0.05) # 20Hz update rate

except KeyboardInterrupt:
    print("\nMeasurement stopped.")