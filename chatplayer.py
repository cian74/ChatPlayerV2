import socket
import time
import threading
import pygame
import vgamepad as vg
from directkeys import PressKey,ReleaseKey,W,A,S,D,SPACE

print(r"""

_________ .__            __ __________.__                              ___.           _________ .__               
\_   ___ \|  |__ _____ _/  |\______   \  | _____  ___.__. ___________  \_ |__ ___.__. \_   ___ \|__|____    ____  
/    \  \/|  |  \\__  \\   __\     ___/  | \__  \<   |  |/ __ \_  __ \  | __ <   |  | /    \  \/|  \__  \  /    \ 
\     \___|   Y  \/ __ \|  | |    |   |  |__/ __ \\___  \  ___/|  | \/  | \_\ \___  | \     \___|  |/ __ \|   |  \
 \______  /___|  (____  /__| |____|   |____(____  / ____|\___  >__|     |___  / ____|  \______  /__(____  /___|  /
        \/     \/     \/                        \/\/         \/             \/\/              \/        \/     \/

 """)

# Read the OAuth key from file
with open('oauthkey.txt', 'r') as file:
    PASS = file.readline().strip()

SERVER = "irc.twitch.tv"
PORT = 6667
BOT = "bot"
CHANNEL = "#cianrr"  # Ensure the channel name is prefixed with '#'
OWNER = "cianrr"

pygame.init()

joysticks = [pygame.joystick.Joystick(x) for x in range (pygame.joystick.get_count())]

for joystick in joysticks:
    joystick.init()
    print("INPUT DEVICE DETECTED:", joystick.get_name())

message = ""
duration = 0
input_condition = 0
lock = threading.Lock()

input_condition = int(input("WHICH INPUT ARE YOU USING- 1-Controller 2-Keyboard: "))

if input_condition == 1:
    gamepad = vg.VDS4Gamepad()

irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send((  "PASS " + PASS + "\r\n" +
            "NICK " + BOT + "\r\n" + 
            "JOIN " + CHANNEL + "\r\n").encode())

for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(0.5)

def gameControl():
    global message, duration, input_condition

    while True:
        with lock:
            msg = message.lower()
            dur = duration
            message = ""
            duration = 0

        if input_condition == 1:
            if "triangle" in msg:
                print(f"Pressing forward for {dur}")
                gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CROSS)
                gamepad.update()
                time.sleep(dur)
                gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE)
                gamepad.update()
            elif "square" in msg:
                print(f"Pressing left for {dur}")
                gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SQUARE)
                gamepad.update()
                time.sleep(dur)
                gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SQUARE)
                gamepad.update()
            elif "cross" in msg:
                print(f"Pressing down for {dur}")
                gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CROSS)
                gamepad.update()
                time.sleep(dur)
                gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CROSS)
                gamepad.update()
            elif "circle" in msg:
                print(f"Pressing right for {dur}")
                gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
                gamepad.update()
                time.sleep(dur)
                gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
                gamepad.update()
            elif "forward" in msg:
                print(f"Pressing forward for {dur}")
                gamepad.left_joystick_float(x_value_float=0.0, y_value_float=-1.0)
                gamepad.update()
                time.sleep(dur)
                gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
                gamepad.update()
            elif "left" in msg:
                print(f"Pressing left for {dur}")
                gamepad.left_joystick_float(x_value_float=-1.0, y_value_float=0.0)
                gamepad.update()
                time.sleep(dur)
                gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
                gamepad.update()
            elif "right" in msg:
                print(f"Pressing right for {dur}")
                gamepad.left_joystick_float(x_value_float=1.0, y_value_float=0.0)
                gamepad.update()
                time.sleep(dur)
                gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
                gamepad.update()
            elif "down" in msg:
                print(f"Pressing down for {dur}")
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

def twitch():
    def joinchat():
        Loading = True
        while Loading:
            readbuffer_join = irc.recv(1024).decode()
            for line in readbuffer_join.split("\n")[0:-1]:
                print(line)
                Loading = loadingComplete(line)

    def loadingComplete(line):
        if "End of /NAMES list" in line:
            print("Bot has joined " + CHANNEL + "'s Channel!")
            sendMessage(irc, "<CHAT PLAYER ENABLED>")
            sendMessage(irc, "MOVEMENT FUNCTIONS: forward, left, right, down")
            return False
        return True
        
    def sendMessage(irc, message):
        messageTmp = "PRIVMSG " + CHANNEL + " :" + message
        irc.send((messageTmp + "\n").encode())

    def getUser(line):
        return line.split(":", 2)[1].split("!", 1)[0] 

    def getMessage(line):
        global message, duration
        try:
            msg = (line.split(":", 2))[2].strip()
            message_parts = msg.rsplit(" ", 1)
            if len(message_parts) > 1 and message_parts[1].isdigit():
                msg = message_parts[0]
                dur = int(message_parts[1])
            #sets default duration to 3 if none is set
            else:
                dur = 3
            if dur > 10:
                dur = 3
        except:
            msg = ""
            dur = 3
        with lock:
            message = msg
            duration = dur
        return msg, dur
    
    #checks that message format is handled
    def checkMessage(irc, msg):
        user_message, dur = getMessage(msg)
        return True
    
    def Console(line):
        return not "PRIVMSG" in line

    joinchat()

    while True:
        try: 
            readbuffer = irc.recv(1024).decode()
        except:
            readbuffer = ""
        for line in readbuffer.split("\r\n"):
            if line == "":
                continue
            elif "PING" in line and Console(line):
                irc.send("PONG tmi.twitch.tv\r\n".encode())
                continue
            else:
                user = getUser(line)
                if checkMessage(irc, line):
                    msg, dur = getMessage(line)
                    print(f"Received message from {user}: {msg} for {dur} seconds")
                    with lock:
                        message = msg
                        duration = dur

if __name__ == '__main__':
    t1 = threading.Thread(target=twitch)
    t1.start()
    t2 = threading.Thread(target=gameControl)
    t2.start()
