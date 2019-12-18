import socket

localIP = "127.0.0.1"
localPort = 20011

TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCPServerSocket.bind((localIP, localPort))
TCPServerSocket.listen(3)
print("TCP server up and listening")
bufferSize = 1024


def put_to_storage(author, succeed):
    with open("index.html", "a") as file:
        status = "SUCCESS" if succeed else "CANCELED"
        file.write("[PET]-[{}]-{}\n".format(status, author))


def is_tolerated(author):
    with open("index.html", "r") as file:
        for line in file.readlines():
            action, status, who = line.split('-')
            if action == '[FEED]':
                if author == who.strip() and status == '[SUCCESS]':
                    return True
    return False


def parse_request(request):
    if request[-1] == '~':
        request = request[:-1]
    authors = request.split("~")
    authors = [x[1:] for x in authors]
    response = ""
    for author in authors:
        if is_tolerated(author):
            response += "Tolerated by the Cat"
            put_to_storage(author, True)
        else:
            response += "Scratched by the Cat"
            put_to_storage(author, False)
    return response


# Listen for incoming datagrams
while True:
    client_socket, addr = TCPServerSocket.accept()
    print("Accepted connection")
    received = client_socket.recv(bufferSize).decode('ascii')
    print("[INFO] Received: " + received)
    full_request = ""
    while received:
        full_request += received

        if received[-1] != '~':
            received = client_socket.recv(bufferSize).decode('ascii')
            print("[INFO] Received: " + received)
        else:
            break

    response = parse_request(full_request)
    print("[INFO] Response: " + response)
    client_socket.send(response.encode('ascii'))
    client_socket.close()
    print("Connection closed!")
