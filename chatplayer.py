import socket
import time
import threading
import pygame
import vgamepad as vg
from directkeys import PressKey,ReleaseKey,W,A,S,D

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
    print(joystick)

message = ""
duration = 0
lock = threading.Lock()

gamepad = vg.VDS4Gamepad()

#TODO: choice between kb vs controller
irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send((  "PASS " + PASS + "\r\n" +
            "NICK " + BOT + "\r\n" + 
            "JOIN " + CHANNEL + "\r\n").encode())

for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(0.5)

#TODO: add keyboard presses - PressKey() - 1
def gameControl():
    global message, duration
    while True:
        with lock:
            msg = message.lower()
            dur = duration
            message = ""
            duration = 0

        if "forward" in msg:
            print(f"Pressing forward for {dur} seconds")
            gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CROSS)
            gamepad.update()
            time.sleep(dur)
            gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE)
            gamepad.update()
        elif "left" in msg:
            print(f"Pressing left for {dur} seconds")
            gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SQUARE)
            gamepad.update()
            time.sleep(dur)
            gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SQUARE)
            gamepad.update()
        elif "down" in msg:
            print(f"Pressing left for {dur} seconds")
            gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CROSS)
            gamepad.update()
            time.sleep(dur)
            gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CROSS)
            gamepad.update()
        elif "right" in msg:
            print(f"Pressing left for {dur} seconds")
            gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
            gamepad.update()
            time.sleep(dur)
            gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
            gamepad.update()
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
            msg = (line.split(":", 2))[2]
            message_parts = msg.rsplit(" ", 1)
            msg = message_parts[0]
            dur = int(message_parts[1])
            if dur > 10:
                dur = 3
        except:
            msg = ""
            dur = 0
        with lock:
            message = msg
            duration = dur
        return msg, dur
    
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
                msg, dur = getMessage(line)
                print(f"Received message from {user}: {msg} for {dur} seconds")

if __name__ == '__main__':
    t1 = threading.Thread(target=twitch)
    t1.start()
    t2 = threading.Thread(target=gameControl)
    t2.start()
