import socket
import threading
import hashlib


class BankAccount :
    def __init__(self, username, password, balance, id):
        ghj = hashlib.sha256(username.encode())
        self.roger = ghj.hexdigest()
        self.username = username
        result = hashlib.sha256(password.encode())
        self.id = id
        self.password = result.hexdigest()
        self.balance = balance
        self.status = False
    def returnbalance(self):
        return self.balance



# creating some sample accounts for bank to bank transfer

acc =[BankAccount("arya","pass",1000,0) , BankAccount("atharva","pass1",100,1)]



PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
HEADER = 64
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
DISCONNECT_MESSAGE = "!disconnect"
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    client_id = -1
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            arr = msg.split(' ')
            if arr[0] == DISCONNECT_MESSAGE:
                connected = False
                client_id = -1
                print(f"[{addr}] {msg}")
                conn.send("Disconneted".encode(FORMAT))
            elif arr[0]== "login":
                for i in acc :
                    if (arr[1]==i.roger and arr[2]==i.password) :
                        i.status =True
                        client_id = i.id
                        # conn.send("LOGIN SUCCESSFULL".encode(FORMAT))
                        print(f"[{addr}] {msg}")
                        break
                if(acc[client_id].status == True):
                    conn.send("...LOGIN SUCCESSFULL...".encode(FORMAT))
                else:
                    conn.send("INVALID USERNAME/PASSWORD".encode(FORMAT))

            elif arr[0] == "accbalance":
                if acc[client_id].status == True:
                    bal = "YOUR ACCOUNT BALANCE IS : RS"+str(acc[client_id].returnbalance())
                    conn.send(bal.encode(FORMAT))
                else:
                    conn.send("[UNAUTHORIZED REQUEST : PLEASE LOGIN]".encode(FORMAT))

            elif arr[0] == "transfer" :
                if acc[client_id].status == True :
                    totransfer = -1
                    flag = False
                    for i in acc :
                        if (arr[1]==i.roger) :

                            totransfer =i.id

                            flag = True
                            print(f"[{addr}] {msg}")
                            break
                    if flag:

                        if int(arr[2]) > acc[client_id].balance:
                            conn.send("[INSUFFICIENT FUNDS]".encode(FORMAT))
                        else:
                            acc[client_id].balance = acc[client_id].balance - int(arr[2])
                            acc[totransfer].balance = acc[totransfer].balance + int(arr[2])
                            conn.send("[TRANSFER SUCCESSFUL]".encode(FORMAT))


                    else:
                        conn.send("[ACCOUNT NOT FOUND]".encode(FORMAT))
                else:
                    conn.send("[UNAUTHORIZED REQUEST : PLEASE LOGIN]".encode(FORMAT))



            else :
                conn.send("[INVALID REQUEST]".encode(FORMAT))

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] server listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client , args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")


print("[STARTING] server is starting")
start()
