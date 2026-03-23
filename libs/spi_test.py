import spidev

for x in range(2):
    spi = spidev.SpiDev()
    spi.open(0, 0) # Bus 0, Device 0 (GPIO 8)
    spi.max_speed_hz = 2000000
    spi.mode = 0b11 # PMW3901 typically requires mode 3

    # Read register 0x00 (Product ID)
    # Send 0x00 and a dummy byte to receive the response
    answer = spi.xfer2([0x00, 0x00])
    print(f"Sensor response (hex): {hex(answer[1])}")

    if answer[1] == 0x49:
        print("SENSOR FOUND! Hardware ID is correct (0x49).")
    else:
        print("No valid response. Check wiring!")
    spi.close()