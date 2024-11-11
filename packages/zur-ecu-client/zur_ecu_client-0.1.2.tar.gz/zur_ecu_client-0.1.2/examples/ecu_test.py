import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 9001

data = b'[[{"bn":"ECU","n":"inverter","vs":"info"}]]'

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    socket.sendto(data, (UDP_IP, UDP_PORT))
    print(f"Send message: {data} to {UDP_IP, UDP_PORT}")
    print(socket.recvfrom(4096))
    time.sleep(1)
