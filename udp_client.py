import socket

serverAddressPort = ("127.0.0.1", 20001)
bufferSize = 1024
# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

msg_parts_collection = [
    [["@Al~0", "ex - M~1", "ilk~"], "Alex", "Milk"],
    [["@007 - Martini~"], "007", "Martini"],
    [["@Zavu~0", "lon1237 ~1", "- Meat~"], "Zavulon1237", "Meat"],
]

for idx, msg_parts_long in enumerate(msg_parts_collection):
    msg_parts, who, eat = msg_parts_long
    print("[ATTEMPT #{}] {} with eat: {}".format(idx, who, eat))
    for msg in msg_parts:
        UDPClientSocket.sendto(str.encode(msg), serverAddressPort)
        msgFromServer, _ = UDPClientSocket.recvfrom(bufferSize)
        print("Message from Server {}".format(msgFromServer))



