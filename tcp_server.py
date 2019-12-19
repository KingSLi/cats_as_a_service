import socket
import threading

localIP = "127.0.0.1"
localPort = 20011

TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCPServerSocket.bind((localIP, localPort))
TCPServerSocket.listen(3)
print("TCP server up and listening")
bufferSize = 1024
cats_scratch_max_time = 3


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


def parse_request(request, count_scratches):
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
            count_scratches += 1
            if count_scratches >= cats_scratch_max_time:
                break
    if count_scratches > cats_scratch_max_time:
        return response, -1
    return response, count_scratches


def handle_client(client_socket, number):
    count_scratches = 0;
    try:
        while True:
            received = client_socket.recv(bufferSize).decode('ascii')
            if received == '':
                break
            print("[INFO] Received: " + received)
            full_request = ""
            while received:
                full_request += received
                if received[-1] != '~':
                    received = client_socket.recv(bufferSize).decode('ascii')
                    print("[INFO] Received: " + received)
                else:
                    break
            response, count_scratches = parse_request(full_request, count_scratches)
            if count_scratches == -1:
                response += "THE CAT RUN AWAY"
            print("[INFO] Response: " + response)
            client_socket.send(response.encode('ascii'))
            if count_scratches == -1:
                break
    finally:
        client_socket.close()
        print("Connection {} closed!".format(number))


# Listen for incoming messages
connection_count = 0
try:
    while True:
        client_socket, addr = TCPServerSocket.accept()
        connection_count += 1
        print("Accepted connection #{}".format(connection_count))
        client_handler = threading.Thread(
            target=handle_client,
            args=(client_socket, connection_count)
        )
        client_handler.start()
finally:
    TCPServerSocket.close()

