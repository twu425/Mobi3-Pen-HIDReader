from ursina import *
from custom_hid import readReports

SENSITIVITY = 0.1
mouse_cursor_sphere = Entity(model='sphere', color=color.red, scale=3, collider='box')
cursor_position = Vec3(0,0,0)

def summon_cube(position):
    cube = Entity(model='cube', color=color.azure, scale=1.5, collider='box')
    cube.position = position
    cube.rotation = (
        random.uniform(0, 360),  # x rotation
        random.uniform(0, 360),  # y rotation
        random.uniform(0, 360)  # z rotation
    )

def update():
    x, y, z, buttons = readReports()

    cursor_position[0] += x * SENSITIVITY
    cursor_position[1] += y * SENSITIVITY
    cursor_position[2] += z * SENSITIVITY

    mouse_cursor_sphere.position = cursor_position
    summon_cube(cursor_position)

app = Ursina()
DirectionalLight().look_at(Vec3(1, -1, 0.5))  # adds shading
EditorCamera()  # add camera controls for orbiting and moving the camera
# camera.position =(0,0,-1000)
app.run()



