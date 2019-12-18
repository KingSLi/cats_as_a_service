import socket

localIP = "127.0.0.1"
localPort = 20001

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

bufferSize = 1024
receive_collector = dict()
allowed_food = ["Fish", "Meat", "Milk", "Bread", "Carrot", "Beer"]


def put_to_storage(author, succeed):
    with open("index.html", "a") as file:
        status = "SUCCESS" if succeed else "CANCELED"
        file.write("[FEED]-[{}]-{}\n".format(status, author))


def get_response(received_message):
    author, food = received_message.split(' - ')
    if food in allowed_food:
        put_to_storage(author, True)
        return "Eaten by the Cat"
    put_to_storage(author, False)
    return "Ignored by the Cat"


# Listen for incoming datagrams
while (True):
    message_byte, address = UDPServerSocket.recvfrom(bufferSize)

    message = message_byte.decode("utf-8")

    if message[-1] == '~':
        receive = receive_collector[address] + message[:-1]
        receive_collector[address] = ""
        print("[INFO] Received message from client with address:{}"
              "\n<----: {}".format(address, receive))
        response = get_response(receive)
    else:
        message, _, attempt = message.rpartition('~')
        if receive_collector.get(address):
            receive_collector[address] += message
        else:
            receive_collector[address] = message[1:]
        response = "The Cat is amused by #{}".format(attempt)

    print("---->: {}".format(response))
    UDPServerSocket.sendto(str.encode(response), address)
