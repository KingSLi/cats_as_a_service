import socket

serverAddressPort = ("127.0.0.1", 20001)
bufferSize = 1024
buff_size_receive = 1024
# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


def send_messages(msg_parts):
    for msg in msg_parts:
        UDPClientSocket.sendto(str.encode(msg), serverAddressPort)
        msg_from_server, _ = UDPClientSocket.recvfrom(buff_size_receive)
        print("[Message from Server] {}".format(msg_from_server.decode("utf-8")))


def run_test():
    msg_parts_collection = [
        [["@Al~0", "ex - M~1", "ilk~"], "Alex", "Milk"],
        [["@007 - Martini~"], "007", "Martini"],
        [["@Zavu~0", "lon1237 ~1", "- Meat~"], "Zavulon1237", "Meat"],
    ]

    for idx, msg_parts_long in enumerate(msg_parts_collection):
        msg_parts, who, eat = msg_parts_long
        print("[ATTEMPT #{}] {} with eat: {}".format(idx, who, eat))
        send_messages(msg_parts)


def create_message(name, food):
    message = "@" + name + " - " + food + "~"
    msgs = [message[x:x + bufferSize]
            for x in range (0, len(message), bufferSize)]
    return [m + ("~" + str(i) if i + 1 != len(msgs) else "")
            for i, m in enumerate(msgs)]


def commands():
    print("/feed - to feed cat")
    print("/test - to send tested messages")
    print("/help - to show commads")
    print("/exit - to close")
    print("/change - to change max message size")


def run_person():
    name = input("Name:")
    food = input("Food:")
    msg_parts = create_message(name, food)
    send_messages(msg_parts)


def main():
    print("You can feed cat!")
    commands()
    while True:
        cmd = input()
        if cmd == '/feed':
            run_person()
        elif cmd == '/test':
            run_test()
        elif cmd == '/exit':
            return
        elif cmd == '/change':
            sz = int(input("New size(max is 1024):"))
            if sz > 1024 or sz <= 0:
                print("Error in new size")
                continue
            global bufferSize
            bufferSize = sz
        else:
            commands()


try:
    main()
finally:
    UDPClientSocket.close()
