import hid
# import pyusb
# 
VID = 0x239A  # Example: Adafruit Pico VID
PID = 0x80F4  # Replace with your board PID

h = hid.device()
h.open(VID, PID)
h.set_nonblocking(True)

# Try reading until we see a report starting with 0x04
while True:
    data = h.read(64)
    if data:
        if data[0] == 4:
            print("Custom HID report:", data)
        else:
            print("Other HID report:", data)