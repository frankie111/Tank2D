import socket


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "192.168.129.44"  # "192.168.1.139"  #   #
        self.port = 5555
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

    def send(self, data: str):
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            print(data)
            print(reply)
            return reply
        except socket.error as e:
            return str(e)
