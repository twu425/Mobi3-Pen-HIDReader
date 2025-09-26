import hid
import struct

VID = 0x239A
PID = 0x80F4
CUSTOM_USAGE_PAGE = 0xFF00
CUSTOM_USAGE = 0x01

device = None
device_connected = False

def find_custom_hid():
    global device, device_connected

    try:
        devices = hid.enumerate(VID, PID)
        custom_hid_info = next(
            d for d in devices if d['usage_page'] == CUSTOM_USAGE_PAGE and d['usage'] == CUSTOM_USAGE
        )

        device = hid.device()
        device.open_path(custom_hid_info['path'])
        device.set_nonblocking(True)
        
        device_connected = True
        print("Opened custom HID:", custom_hid_info['product_string'])

        return device
    
    except StopIteration:
        # Device not found
        device_connected = False
        return None
    except OSError as e:
        print("Error opening device:", e)
        device_connected = False
        return None
    
def readReports():

    global device, device_connected

    # If device not connected, try to reconnect
    if not device_connected or device is None:
        device = find_custom_hid()
        if device is None:
            return 0, 0, 0, 0  # no movement
        

    summed_x = summed_y = summed_z = 0
    buttons = 0 # TODO: Add button support

    try:
        # Accumulate mouse movement
        while True:
            report = device.read(17)
            if not report:
                break  # no more queued reports this frame

            report_id, dx, dy, dz, buttons, r1, r2, r3 = struct.unpack('<BbbbBfff', bytes(report))

            # relative movement: accumulate
            summed_x += dx
            summed_y += dy
            summed_z += dz

    except OSError:
        # Device disconnected during read
        print("Device disconnected!")
        device.close()
        device_connected = False
        device = None
        return 0, 0, 0, 0
    
    return summed_x, summed_y, summed_z, buttons


def print_hid_devices():
    for d in hid.enumerate():
        print(f"VID: {d['vendor_id']:04X}, PID: {d['product_id']:04X}, "
            f"Product: {d['product_string']}, Manufacturer: {d['manufacturer_string']}")

