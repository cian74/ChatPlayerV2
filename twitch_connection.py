import socket
import time
import concurrent.futures

class Twitch:
    def __init__(self, server="irc.chat.twitch.tv", port=6667, channel="#cianrr", bot="bot"):
        self.server = server
        self.port = port
        self.channel = channel
        self.bot = bot
        self.message = ""
        self.duration = 0
        self.message_counter = 0

        # Load OAuth key from file
        try:
            with open('oauthkey.txt', 'r') as file:
                self.oauth_key = file.readline().strip()
        except FileNotFoundError:
            print("Error: oauthkey.txt not found. Please create the file and add your OAuth key from https://twitchapps.com/tmi/")
            raise
        except Exception as e:
            print(f"Error reading oathkey.txt {e}")

        self.irc = socket.socket()
        self.connect()

        self.exucutor = concurrent.futures.ThreadPoolExecutor(max_workers=100)

        self.send_message("Connected to chat!.")

    def connect(self):
        """Connect to the Twitch IRC server and join the channel."""
        try:
            self.irc.connect((self.server, self.port))
            self.irc.send((f"PASS {self.oauth_key}\r\nNICK {self.bot}\r\nJOIN {self.channel}\r\n").encode())
            print(f"Connecting to {self.channel}'s channel...")
        except socket.error as e:
            print(f"Error connecting to {self.channel}'s channel: {e}")
            raise

    def send_message(self, message):
        """Send a message to the Twitch chat."""
        message_tmp = f"PRIVMSG {self.channel} :{message}"
        self.irc.send((message_tmp + "\n").encode())

    def receive_message(self):
        """Receive a message from the Twitch IRC server."""
        try:
            readbuffer = self.irc.recv(1024).decode()
        except socket.error:
            return None

        messages = readbuffer.split("\r\n")
        for line in messages:
            if line == "":
                continue
            if "PING" in line:
                self.irc.send("PONG tmi.twitch.tv\r\n".encode())
            else:
                return line
        return None

    def process_message(self, line):
        """Extract and return the message and duration from a Twitch chat message."""
        try:
            msg = (line.split(":", 2))[2].strip().lower()
            message_parts = msg.rsplit(" ", 1)
            if len(message_parts) > 1 and message_parts[1].isdigit():
                msg = message_parts[0]
                dur = int(message_parts[1])
            else:
                dur = 3
            if dur > 10:
                dur = 3
        except IndexError:
            msg = ""
            dur = 3
        return msg, dur