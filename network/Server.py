import socket
from _thread import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "192.168.1.139"
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for connection")

currentId = "0"
pos = ["0:100,100,0", "1:100,100,0"]


def threaded_client(connection):
    global currentId, pos
    connection.send(str.encode(currentId))
    currentId = "1"
    reply = ''

    while True:
        try:
            data = connection.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                connection.send(str.encode("Goodbye"))
                break
            else:
                print(f"Recieved: {reply}")
                arr = reply.split(":")
                curr_id = int(arr[0])
                pos[curr_id] = reply

                next_id = 1 if curr_id == 0 else 0

                reply = pos[next_id][:]
                print(f"Sending: {reply}")

            connection.sendall(str.encode(reply))
        except socket.error as err:
            print(str(err))

    print("Connection Closed")
    connection.close()


while True:
    conn, addr = s.accept()
    print(f"Connected to: {addr}")

    start_new_thread(threaded_client, (conn,))
