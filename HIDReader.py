import hid
from ursina import *
import struct

for d in hid.enumerate():
    print(f"VID: {d['vendor_id']:04X}, PID: {d['product_id']:04X}, "
          f"Product: {d['product_string']}, Manufacturer: {d['manufacturer_string']}")

VID = 0x239A
PID = 0x80F4
CUSTOM_USAGE_PAGE = 0xFF00
CUSTOM_USAGE = 0x01

# Enumerate devices
devices = hid.enumerate(VID, PID)
for d in devices:
    print(d['product_string'], "usage_page:", d['usage_page'], "usage:", d['usage'], "path:", d['path'])

# Pick the device with vendor-defined usage page
custom_hid_info = next(d for d in devices if d['usage_page'] == CUSTOM_USAGE_PAGE and d['usage'] == CUSTOM_USAGE)

# Open using path
device = hid.device()
device.open_path(custom_hid_info['path'])
print("Opened custom HID:", custom_hid_info['product_string'])

mouse_cube = Entity(model='sphere', color=color.red, scale=3, collider='box')

my_position = Vec3(0,0,0)
def update():
    report = device.read(17)  # 16 bytes + 1 byte for report ID if needed
    report_id, x, y, z, buttons, fx, fy, fz = struct.unpack('<BbbbBfff', bytes(report))
    print(x)
    my_position[0] += x / 10
    my_position[1] += z / 10
    my_position[2] += y / 10
    # print(report)
    # print(my_position)
    # print(fx, fy, fz)
    cube = Entity(model='cube', color=color.azure, scale=1.5, collider='box')
    cube.position = my_position
    cube.rotation = (
        random.uniform(0, 360),  # x rotation
        random.uniform(0, 360),  # y rotation
        random.uniform(0, 360)  # z rotation
    )
    mouse_cube.rotation = (
        random.uniform(0, 360),  # x rotation
        random.uniform(0, 360),  # y rotation
        random.uniform(0, 360)  # z rotation
    )
    mouse_cube.position = my_position
    return report


app = Ursina()
DirectionalLight().look_at(Vec3(1, -1, 0.5))  # adds shading
position = (0, 0, 0)


# def spin():
#     cube.animate('rotation_y', cube.rotation_y+360, duration=2, curve=curve.in_out_expo)

# cube.on_click = spin
EditorCamera()  # add camera controls for orbiting and moving the camera
# camera.position =(0,0,-1000)
app.run()

# try:
#     # Open the HID device
#     device = hid.device()
#     device.open(VID, PID)
#     print(f"Connected to HID device VID={VID:04x} PID={PID:04x}")
#
#     # Optional: set non-blocking mode
#     device.set_nonblocking(True)
#
#     print("Dumping HID reports (press Ctrl+C to stop):")
#     while True:
#         try:
#             report = device.read(64)
#             if report:
#                 print("Report:", report)
#         except KeyboardInterrupt:
#             print("\nStopping...")
#             break
#
# except IOError as e:
#     print(f"Failed to open HID device: {e}")
#
