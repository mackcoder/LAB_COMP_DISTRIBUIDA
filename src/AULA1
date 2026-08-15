# User in Auction
# Naoto Ushizaki - 10437445 - 06G

import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

def receive_messages(client):

    try:
        while True:
            data = client.recv(4096)

            if not data:
                print("\nServidor encerrou a conexao.")
                break

            # Pode ter um aou mais mensagens no mesmo recv
            messages = data.decode("utf-8").splitlines()

            for message in messages:
                print(f"\nUPDATE: {message}")

    except OSError:
        pass

def main():
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    client.connect((HOST, PORT))

    # Thread exclusiva para receber broadcasts
    receiver_thread = threading.Thread(target=receive_messages,args=(client,),daemon=True)

    receiver_thread.start()

    try:
        while True:
            bid = input("PLACE YOUR BID: ").strip()

            if not bid:
                continue
            # Codificando msm e mandando para server
            client.sendall((bid + "\n").encode("utf-8"))

            if bid.upper() == "SAIR":
                break

    except KeyboardInterrupt:
        print("\nCliente encerrado.")

    finally:
        client.close()


if __name__ == "__main__":
    main()