import asyncio
from bleak import BleakScanner, BleakClient
import vgamepad as vg

# Config
address = "A4:34:F1:7F:24:9F"
service = "08590f7e-db05-467e-8757-72f6faeb13a5"
characteristic = "08590f7e-db05-467e-8757-72f6faeb1336"

# Gamepad
gamepad = vg.VX360Gamepad()

def notification_handler(sender, data):
    # Here is how controller is divided up:
    # First byte is the y-axis of left joystick (full up is 0, full down is 255)
    # Second byte is the x-axis of left joystick (full right is 0, full left is 255)
    # Third byte is the y-axis of right joystick (full up is 0, full down is 255)
    # Fourth byte is the x-axis of right joystick (full right is 0, full left is 255)
    # Fifth byte is the dpad + l1 and r1 (down adds 1, right adds 2, up adds 4, left adds 8, r1 adds 16, l1 adds 32)
    # Sixth byte is abxy + l2 and r2 + home (y adds 1, b adds 2, a adds 4, x adds 8, l2 adds 16, r2 adds 32, home adds 128)

    # Parse Left Joystick (convert range from 0-255 to -32768-32767)
    left_y = data[0]
    left_x = data[1]

    # Parse Right Joystick (convert range from 0-255 to -32768-32767)
    right_y = data[2]
    right_x = data[3]

    # Parse Dpad
    dpad = data[4]
    dpad_down = dpad % 2
    dpad_right = (dpad // 2) % 2
    dpad_up = (dpad // 4) % 2
    dpad_left = (dpad // 8) % 2
    r1 = (dpad // 16) % 2
    l1 = (dpad // 32) % 2

    # Parse Buttons
    buttons = data[5]
    y = buttons % 2
    b = (buttons // 2) % 2
    a = (buttons // 4) % 2
    x = (buttons // 8) % 2
    l2 = (buttons // 16) % 2
    r2 = (buttons // 32) % 2
    home = (buttons // 128) % 2

    # Set Joysticks
    gamepad.left_joystick_float((left_x-127)/127, (left_y-127)/127)
    gamepad.right_joystick_float((right_x-127)/127, (right_y-127)/127)

    # Set Dpad
    if dpad_down:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
    
    if dpad_right:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
    
    if dpad_up:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
    
    if dpad_left:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
    
    # Set ABXY
    if a:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    
    if b:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    
    if x:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    
    if y:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)

    # Set bumpers
    if l1:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    
    if r1:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    
    # Set triggers
    gamepad.left_trigger_float(l2)
    gamepad.right_trigger_float(r2)

    # Set home button
    if home:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
    
    print("Updated controller")



async def run():
    # Connect to the device
    controller = BleakClient(address)
    await controller.connect()
    # Subscribe to the characteristic
    await controller.start_notify(characteristic, notification_handler)

# Run forever
loop = asyncio.get_event_loop()
loop.run_until_complete(run())
loop.run_forever()

