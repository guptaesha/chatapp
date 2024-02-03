import socket
import random

from threading import Thread
from datetime import datetime
from colorama import Fore,init,Back


init()
colors=[Fore.BLUE,Fore.CYAN,Fore.GREEN,Fore.LIGHTBLACK_EX]

client_color=random.choice(colors)

server_host='127.0.0.5'
server_port=5003
separator_token='<SEP>'

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {server_host}:{server_port}...")
# connect to the server
s.connect((server_host, server_port))
print("[+] Connected.")

# prompt the client for a name
name = input("Enter your name: ")

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)

# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()

while True:
    # input message we want to send to the server
    to_send =  input()
    # a way to exit the program
    if to_send.lower() == 'q':
        break
    # add the datetime, name & the color of the sender
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
    # finally, send the message
    s.send(to_send.encode())

# close the socket
s.close()