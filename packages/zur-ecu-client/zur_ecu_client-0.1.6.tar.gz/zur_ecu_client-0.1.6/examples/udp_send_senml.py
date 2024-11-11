import socket
import json

# ECU IP & Port
UDP_IP = "127.0.0.1"
UDP_PORT = 9001

# SenML message to be send
data = [
    [
        {"bn": "ECU", "n": "driverless", "vs": "control"},
        {"n": "steeringAngle", "u": "°", "v": -2000},
    ]
]
MESSAGE = json.dumps(data)

# Open socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send message
sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
print(f"Send msg: {MESSAGE}")

# Receive message
response, addr = sock.recvfrom(1024)
response = response.decode()
print(f"Received msg: {response}")
