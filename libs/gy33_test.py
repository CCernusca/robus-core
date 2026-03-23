import time
from smbus2 import SMBus

# I2C address of the GY-33
ADDR = 0x5A

# Register definitions (per datasheet)
REG_RGB_START = 0x05  # Start register for R, G, B data
REG_LUX = 0x11        # Register for brightness

bus = SMBus(1) # Bus 1 on Raspberry Pi 5

def read_color():
    try:
        # Read 3 bytes from register 0x05 (red, green, blue)
        data = bus.read_i2c_block_data(ADDR, REG_RGB_START, 3)
        r = data[0]
        g = data[1]
        b = data[2]

        # Read brightness (lux) - typically 2 bytes
        lux_data = bus.read_i2c_block_data(ADDR, REG_LUX, 2)
        lux = (lux_data[0] << 8) | lux_data[1]

        return r, g, b, lux
    except Exception as e:
        print(f"Error reading sensor: {e}")
        return None

print("GY-33 color measurement started...")

try:
    while True:
        result = read_color()
        if result:
            r, g, b, lux = result
            print(f"R: {r:3} | G: {g:3} | B: {b:3} | Brightness: {lux} lux")

            # Optional: simple color detection
            if r > g and r > b:
                print("Dominant color: RED")
            elif g > r and g > b:
                print("Dominant color: GREEN")
            elif b > r and b > g:
                print("Dominant color: BLUE")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nMeasurement stopped.")