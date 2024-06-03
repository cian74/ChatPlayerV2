import socket
from directkeys import PressKey,ReleaseKey, W, A, S, D 
import threading
import time
SERVER = "irc.twitch.tv"
PORT = 6667
PASS = "TWITCHOAUTHPASS"
BOT = "bot"
CHANNEL = "#cianrr"  # Ensure the channel name is prefixed with '#'
OWNER = "cianrr"

message = ""
duration = 0

irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send((  "PASS " + PASS + "\r\n" +
            "NICK " + BOT + "\r\n" + 
            "JOIN " + CHANNEL + "\r\n").encode())

for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(0.5)

def gameControl():
    global message, duration
    while True:
        if "forward" in message.lower():
            PressKey(W)
            time.sleep(duration)
            ReleaseKey(W)
            message = ""
            duration = 0
        elif "left" in message.lower():
            PressKey(A)
            time.sleep(duration)
            ReleaseKey(A)
            message = ""
            duration = 0
        elif "down" in message.lower():
            PressKey(S)
            time.sleep(duration)
            ReleaseKey(S)
            message = ""
            duration = 0
        elif "right" in message.lower():
            PressKey(D)
            time.sleep(duration)
            ReleaseKey(D)
            message = ""
            duration = 0
        else:
            pass

def twitch():
    def joinchat():
        Loading = True
        while Loading:
            readbuffer_join = irc.recv(1024)
            readbuffer_join = readbuffer_join.decode()
            for line in readbuffer_join.split("\n")[0:-1]:
                print(line)
                Loading = loadingComplete(line)

    def loadingComplete(line):
        if ("End of /NAMES list" in line):  # Adjusted the join confirmation check
            print("Bot has joined " + CHANNEL + "'s Channel!")
            sendMessage(irc, "<CHAT PLAYER ENABLED>")
            sendMessage(irc, "MOVEMENT FUNCTIONS: forward, left, right, down")
            return False
        else:
            return True
        
    def sendMessage(irc, message):
        messageTmp = "PRIVMSG " + CHANNEL + " :" + message
        irc.send((messageTmp + "\n").encode())

    def getUser(line):
        seperate = line.split(":", 2)
        user = seperate[1].split("!", 1)[0] 
        return user

    def getMessage(line):
        global message, duration
        try:
            message = (line.split(":", 2))[2]
            message_parts = message.rsplit(" ", 1)
            message = message_parts[0]
            duration = int(message_parts[1])
            if duration > 10:
                duration = 3
        except:
            message = ""
            duration = 0
        return message , duration
    
    def Console(line):
        if "PRIVMSG" in line:
            return False
        else:
            return True

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
                msgg = "PONG tmi.twitch.tv\r\n".encode() # have to return a pong to stay connectedd
                irc.send(msgg)
                print(msgg)
                continue
            else:
                user = getUser(line)
                message, duration = getMessage(line)
                print(user + " : " + message)

if __name__ == '__main__':
    t1 = threading.Thread(target = twitch)
    t1.start()
    t2 = threading.Thread(target = gameControl)
    t2.start()