import spidev

class ADNS3080:
    def __init__(self, bus=0, device=0):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 2000000
        self.spi.mode = 3 # ADNS3080 typically uses mode 3

        # Check sensor (product ID should be 0x17)
        pid = self.read_register(0x00)
        if pid != 0x17:
            print(f"WARNING: ADNS3080 not recognized! ID: {hex(pid)}")
        else:
            print("ADNS3080 successfully recognized.")

        # Configuration (optional): set resolution to 1600 cpi
        # Register 0x09: set bit 4 for high resolution, set bit 5A
        self.write_register(0x0a, 0x10) # Configuration_bits

    def read_register(self, addr):
        # MSB must be 0 for read (standard, but we send the address)
        resp = self.spi.xfer2([addr, 0x00])
        return resp[1]

    def write_register(self, addr, value):
        # MSB must be 1 for write
        self.spi.xfer2([addr | 0x80, value])

    def get_motion(self):
        # Read motion register (0x02)
        # If bit 7 (0x80) is set, motion was detected
        motion = self.read_register(0x02)

        if motion & 0x80:
            # Read delta X and Y
            dx = self.read_register(0x03)
            dy = self.read_register(0x04)

            # Convert to signed integer (8-bit two's complement)
            if dx > 127: dx -= 256
            if dy > 127: dy -= 256
            
            return dx, dy
        return 0, 0