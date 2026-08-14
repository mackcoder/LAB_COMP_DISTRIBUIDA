# Server Auction
# Naoto Ushizaki - 10437445 - 06G
 
import socket
import logging
import threading # biblioteca para simular paralelismo

Proprietor = "0.0.0.0"
PORT = 5000
MAX_USERS = 5

# Criando listas e locks:
clients = {}
client_lock = threading.Lock()
auction_lock = threading.Lock()

# Vars globais:
best_bid = 0.0
winning_user = None
finished_auction = None

# Mandar msm para todos:
def send_all(msg):
    data = (msg + "\n".encode("utf-8"))

    with client_lock:
        active_users = list(clients.items())

        for conn, name in active_users:
            try:
                conn.sendall(data)
            except OSError:
                logging.warning("ERROR - MESSAGE NOT SENT TO {name}", name)

def mult_client(conn, addr):
    name = f"({addr[0]} : {addr[1]})"

    with client_lock:
        clients[conn] = name

    logging.info("CLIENT CONNECTED -> %s", name)

    conn.sendall(
        (
            "CONNECTED TO AUCTION SERVER 2026\n"
            "USE LANCE;PRECO OU sair\n"
        ).encode("utf-8")
    )

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            input = data.decode("utf-8").strip()
            response = auction_system(name, input)
            conn.sendall((response + "\n").encode("utf-8"))

            logging.info("REQUEST FROM %s: %s", name, input)

            if input.upper() == "ENCERRAR":
                break

    except ConnectionResetError:
        logging.info(
            "CLIENT CONNECTION RESET: %s", name)

    finally:
        with client_lock:
            clients.pop(conn, None)
        conn.close()
        logging.info(
            "CLIENT DISCONNECTED: %s", name)

def process_bid(name, bid):
    global best_bid
    global winning_user

    # processando input de user:
    texto = texto.strip().replace(",", ".")

    try:
        valor = float(texto)

    except ValueError:
        return (
            "ERRO: Digite somente um valor numerico. "
            "Exemplo: 500.00"
        )

    if valor <= 0:
        return "ERRO: O valor deve ser maior que zero."
    
    with auction_lock:
        if finished_auction:
            return "ERROR - EVENT TERMINATED"

        if bid <= best_bid:
            return f"INVALID BID - MUST BE HIGHER THAN {best_bid}"
        # Atualizando usuário ganhando no momento e oferta mais alta:
        best_bid = bid
        winning_user = name

        notification = (f"NEW BID -> {name} made a bid of {bid:.2f}$")

        send_all(notification)

    return "OFFER MADE"

def auction_system(name, input):

    global auction_lock

    input = input.strip()

    if input.upper() == "sair":
        with auction_lock:
            if finished_auction:
                return "ERROR - Leilao encerrado"
            finished_auction = True
            bid = best_bid
            winner = winning_user

        if winner is None:
            msm = "NO BIDS WERE REGISTERED"
        else:
            msm = (f"AUCTION TERMINATED - SOLD TO {winner} for {bid}$")

        send_all(msm)

        return "AUCTION CLOSED!"

    return process_bid(name, msm)

def main():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")

    # Iniciando conexão Server <-> User
    host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host.bind((Proprietor, PORT))
    host.listen(5) # Fila pequena para demonstrar o limite

    print("MAIN CONSOLE - INITIATING AUCTION 2026")
    print(f"Server listening by {PORT}...")

    users_connected = list()

    while True:
        connect, addr = host.accept()

        with client_lock:
            quant = len(users_connected)

        if quant > MAX_USERS:
            connect.sendall(("ERROR -> LIMIT EXCEDED.\n").encode("utf-8"))
            connect.close()

            logging.warning("Conexao recusada: limite de clientes atingido")
            continue
        # Paralelizando clientes:
        parallel_user = threading.Thread(target = mult_client, args = (connect, addr), daemon = True)
        parallel_user.start()

        logging.info("\n --- Thread criada para %s", addr)
    
if __name__ == "__main__":
    main()
