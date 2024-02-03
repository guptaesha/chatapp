import socket
from threading import Thread

server_host='127.0.0.1'
server_port=5003
separator_token='<SEP>'

client_sockets=set()

s=socket.socket()

# s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

s.bind((server_host,server_port))

s.listen(5)
print(f"[*] Listening as {server_host}:{server_port}")

def listen_for_client(cs):
    while True:
        try:
            msg=cs.recv(1024).decode()
        
        except Exception as e:
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        
        else:
            msg = msg.replace(separator_token, ": ")
        # iterate over all connected sockets
        for client_socket in client_sockets:
            # and send the message
            client_socket.send(msg.encode())
while True:
    # we keep listening for new connections all the time
    
    client_socket, client_address = s.accept()
    
    print(f"[+] {client_address} connected.")
    # add the new connected client to connected sockets
    client_sockets.add(client_socket)
    # start a new thread that listens for each client's messages
    t = Thread(target=listen_for_client, args=(client_socket,))
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()

# close client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()
