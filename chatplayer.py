import time
import pygame
import vgamepad as vg
from directkeys import PressKey, ReleaseKey, W, A, S, D, SPACE
import twitch_connection
import concurrent.futures
import keyboard

print(r"""

_________ .__            __ __________.__                              ___.           _________ .__               
\_   ___ \|  |__ _____ _/  |\______   \  | _____  ___.__. ___________  \_ |__ ___.__. \_   ___ \|__|____    ____  
/    \  \/|  |  \\__  \\   __\     ___/  | \__  \<   |  |/ __ \_  __ \  | __ <   |  | /    \  \/|  \__  \  /    \ 
\     \___|   Y  \/ __ \|  | |    |   |  |__/ __ \\___  \  ___/|  | \/  | \_\ \___  | \     \___|  |/ __ \|   |  \
 \______  /___|  (____  /__| |____|   |____(____  / ____|\___  >__|     |___  / ____|  \______  /__(____  /___|  /
        \/     \/     \/                        \/\/         \/             \/\/              \/        \/     \/

 """)

pygame.init()

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

for joystick in joysticks:
    joystick.init()
    print("INPUT DEVICE DETECTED: ", joystick.get_name(), ", VIA: ", joystick.get_power_level(), ", GUID:", joystick.get_guid())

thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=100)
message = ""
duration = 0
message_counter = 0
input_condition = 0
active_tasks = []

t = twitch_connection.Twitch()


input_condition = int(input("WHICH INPUT ARE YOU USING- 1-Controller 2-Keyboard: "))

if input_condition == 1:
    gamepad = vg.VDS4Gamepad()

for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(0.5)
    
print(f"connected to channel: {t.channel}")

def gameControl(msg,dur):
    global input_condition

    if input_condition == 1:
        if "triangle" in msg:
            print(f"[",joystick.get_name(),"]",f"triangle for {dur}")
            gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE)
            gamepad.update()
            time.sleep(dur)
            gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE)
            gamepad.update()
        elif "square" in msg:
            print(f"[",joystick.get_name(),"]",f"square for {dur}")
            gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SQUARE)
            gamepad.update()
            time.sleep(dur)
            gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SQUARE)
            gamepad.update()
        elif "cross" in msg:
            print(f"[",joystick.get_name(),"]",f"cross for {dur}")
            gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CROSS)
            gamepad.update()
            time.sleep(dur)
            gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CROSS)
            gamepad.update()
        elif "circle" in msg:
            print(f"[",joystick.get_name(),"]",f"circle for {dur}")
            gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
            gamepad.update()
            time.sleep(dur)
            gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
            gamepad.update()
        elif "forward" in msg:
            print(f"[",joystick.get_name(),"]",f"forward for {dur}")
            gamepad.left_joystick_float(x_value_float=0.0, y_value_float=-1.0)
            gamepad.update()
            time.sleep(dur)
            gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
            gamepad.update()
        elif "left" in msg:
            print(f"[",joystick.get_name(),"]",f"left for {dur}")
            gamepad.left_joystick_float(x_value_float=-1.0, y_value_float=0.0)
            gamepad.update()
            time.sleep(dur)
            gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
            gamepad.update()
        elif "right" in msg:
            print(f"[",joystick.get_name(),"]",f"right for {dur}")
            gamepad.left_joystick_float(x_value_float=1.0, y_value_float=0.0)
            gamepad.update()
            time.sleep(dur)
            gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
            gamepad.update()
        elif "down" in msg:
            print(f"[",joystick.get_name(),"]",f"down for {dur}")
            gamepad.left_joystick_float(x_value_float=0.0, y_value_float=1.0)
            gamepad.update()
            time.sleep(dur)
            gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
            gamepad.update()

    elif input_condition == 2:
        if "forward" in msg:
            print(f"Pressing forward for {dur}")
            PressKey(W)
            time.sleep(dur)
            ReleaseKey(W)
        elif "left" in msg:
            print(f"Pressing left for {dur}")
            PressKey(A)
            time.sleep(dur)
            ReleaseKey(A)
        elif "down" in msg:
            print(f"Pressing down for {dur}")
            PressKey(S)
            time.sleep(dur)
            ReleaseKey(S)
        elif "right" in msg:
            print(f"Pressing right for {dur}")
            PressKey(D)
            time.sleep(dur)
            ReleaseKey(D)
        elif "space" in msg:
            print(f"Pressing space for {dur}")
            PressKey(SPACE)
            time.sleep(dur)
            ReleaseKey(SPACE)
        time.sleep(0.1)

def handle_messages():
    while True:
        line = t.receive_message()
        if line:
            message, duration = t.process_message(line)
            if message and duration:
                print(f"Messsage: {message}, Duration: {duration}")
            
                active_tasks.append(thread_pool.submit(gameControl, message, duration))
        if not line:
            print("could not receive message")
                
    
thread_pool.submit(handle_messages)

while True:
    if keyboard.is_pressed("shift+backspace"):
        print("Exiting...")
        exit()