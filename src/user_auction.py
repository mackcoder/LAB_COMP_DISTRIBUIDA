# User in Auction
# Naoto Ushizaki - 10437445 - 06G

import socket

HOST = "127.0.0.1"
PORT = 5000

def main():
    # INIT conexão:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST,PORT))
    # Recebe msm do server
    msg = client.recv(4096)
    print(msg.decode("utf-8").strip())

    while True:
        bid = input("PLACE YOUR BID: ").strip()

        if not bid:
            continue
        # Mandando input para server
        client.sendall((bid + "\n").encode("utf-8"))

        response = client.recv(4096)
        if not response:
            break

        print("UPDATE: ", response.decode("utf-8").strip())

    client.close()

if __name__ == "__main__":
    main()