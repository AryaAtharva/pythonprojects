import socket
import hashlib
import time

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
HEADER = 64
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!disconnect"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
    print("[SERVER MESSAGE]:")
    print(client.recv(2048).decode(FORMAT))
    time.sleep(2)

connected = True
while connected :
    print("----------------------------------------------")
    print("1. Login into account ")
    print("2. Get account balance")
    print("3. Transfer money to other account")
    print("4. Logout")
    print("Enter your option ")
    option = int(input())
    if option == 1 :
        user = str(input("Enter Username :"))
        userx= hashlib.sha256(user.encode())
        password = str(input("Enter password :"))
        result = hashlib.sha256(password.encode())
        msg_sent ="login "+userx.hexdigest() +" "+result.hexdigest()
        send(msg_sent)
    if option == 2 :
        send("accbalance")
    if option == 3 :
        username = str(input("Enter Username :"))
        usernamex= hashlib.sha256(username.encode())
        amt = str(input("Enter amount to be transferred:"))
        card = str(input("Enter card number:"))
        trans = "transfer " +usernamex.hexdigest() + " "+amt
        send(trans)
    if option == 4 :
        connected = False

send(DISCONNECT_MESSAGE)
