import socket

serverAddressPort = ("127.0.0.1", 20011)
bufferSize = 1024
# Create a TCP socket at client side
TCPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)


def send_messages(messages):
    for msg in messages:
        TCPClientSocket.send(msg.encode('ascii'))
    response = TCPClientSocket.recv(bufferSize).decode('ascii')
    print("Response: " + response)


TCPClientSocket.connect(serverAddressPort)
print("Connected to TCP server")
messages = ["@Zavu", "lon1237~", "@Alex~@00", "7~@Alex~@Alex~@Alex~@Alex~"]
send_messages(messages)
TCPClientSocket.close()
print("Connection closed!")
