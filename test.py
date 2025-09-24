import hid

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