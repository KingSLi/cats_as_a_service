import socket

serverAddressPort = ("127.0.0.1", 20011)
bufferSize = 1024
# Create a TCP socket at client side
TCPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)


def send_messages(messages):
    for msg in messages:
        TCPClientSocket.send(msg.encode('ascii'))
    response = TCPClientSocket.recv(bufferSize).decode('ascii')
    print("[Server Message] " + response)
    if len(response) > len("THE CAT RUN AWAY") and response.endswith("THE CAT RUN AWAY"):
        return False
    return True


def send_message(message):
    TCPClientSocket.send(message.encode('ascii'))
    response = TCPClientSocket.recv(bufferSize).decode('ascii')
    print("[Server Message] " + response)
    if len(response) > len("THE CAT RUN AWAY") and response.endswith("THE CAT RUN AWAY"):
        return False
    return True


def commands():
    print("/pet - to pet cat")
    print("/test - to send tested messages")
    print("/help - to show commads")
    print("/exit - to close")


def run_person():
    name = input("Name:")
    msg = "@" + name + "~"
    return send_message(msg)


def run_test():
    messages = ["@Zavu", "lon1237~", "@Alex~@00", "7~@Alex~@Alex~@Alex~@Alex~"]
    return send_messages(messages)


def main():
    TCPClientSocket.connect(serverAddressPort)
    print("Connected to TCP server")
    while True:
        cmd = input()
        if cmd == '/pet':
            if not run_person():
                break
        elif cmd == '/test':
            if not run_test():
                break
        elif cmd == '/exit':
            break
        else:
            commands()
    TCPClientSocket.close()
    print("Connection closed!")


main()
