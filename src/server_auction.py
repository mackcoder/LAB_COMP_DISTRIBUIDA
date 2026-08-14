# Server Auction
# Naoto Ushizaki - 10437445 - 06G

import socket
import logging
import threading


HOST = "0.0.0.0"
PORT = 5000
MAX_USERS = 5


# Clientes conectados
clients = {}
client_lock = threading.Lock()

# Protege best_bid e winning_user
auction_lock = threading.Lock()

# Variáveis globais do leilão
best_bid = 0.0
winning_user = None
finished_auction = False

def send_all(message):

    data = (message + "\n").encode("utf-8")

    # Copia os clientes antes de enviar mensagens.
    with client_lock:
        active_users = list(clients.items())

    for conn, name in active_users:
        try:
            conn.sendall(data)

        except OSError:
            logging.warning("ERROR - MESSAGE NOT SENT TO %s", name)

def process_bid(name, text):

    global best_bid
    global winning_user

    text = text.strip().replace(",", ".")

    try:
        bid = float(text)

    except ValueError:
        return (
            "ERRO: Digite somente um valor numerico. "
            "Exemplo: 500.00"
        )

    if bid <= 0:
        return "ERRO: O valor deve ser maior que zero."

    # Apenas uma thread compara e atualiza o lance por vez
    with auction_lock:
        if finished_auction:
            return "ERRO: LEILAO ENCERRADO"

        if bid <= best_bid:
            return "LANCE RECUSADO: Valor baixo"

        best_bid = bid
        winning_user = name

        notification = (
            f"Novo lance, R$ {best_bid:.2f} "
            f"por {winning_user}"
        )

    # Broadcast fora do auction_lock
    send_all(notification)

    return "LANCE ACEITO"

def close_auction():

    global finished_auction

    with auction_lock:
        if finished_auction:
            return "ERRO: LEILAO JA ENCERRADO"
        # Decidindo que ganhou e qual preço no momento:
        finished_auction = True
        final_bid = best_bid
        winner = winning_user

    if winner is None:
        message = "LEILAO ENCERRADO: Nenhum lance registrado."
    else:
        message = (
            f"LEILAO ENCERRADO: Vencedor {winner} "
            f"com R$ {final_bid:.2f}")

    send_all(message)
    return "LEILAO ENCERRADO"

def auction_system(name, message):
    message = message.strip()

    if message.upper() == "SAIR":
        return close_auction()

    # Tudo que não for SAIR é tratado como valor de lance
    return process_bid(name, message)

# Funcao cuidando de varios clientes conectados:
def mult_client(conn, addr):

    name = f"{addr[0]}:{addr[1]}"

    with client_lock:
        clients[conn] = name

    logging.info("CLIENT CONNECTED -> %s", name)

    conn.sendall(
        (
            "CONNECTED TO AUCTION SERVER 2026\n"
            "Digite somente o valor do lance.\n"
            "Exemplo: 500.00\n"
            "Digite SAIR para encerrar.\n").encode("utf-8"))

    try:
        while True:
            data = conn.recv(1024)

            # b"" indica que o cliente fechou a conexão
            if not data:
                break

            message = data.decode("utf-8").strip()

            response = auction_system(name, message)

            # Resposta individual ao cliente que enviou o lance
            conn.sendall((response + "\n").encode("utf-8"))

            logging.info("REQUEST FROM %s: %s", name,message)

            if message.upper() == "SAIR":
                break

    except ConnectionResetError:
        logging.info(
            "CLIENT CONNECTION RESET: %s", name)

    finally:
        with client_lock:
            clients.pop(conn, None)

        conn.close()

def main():
    logging.basicConfig(format="%(asctime)s: %(message)s",level=logging.INFO,datefmt="%H:%M:%S")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    server.bind((HOST, PORT))
    server.listen(MAX_USERS)

    print("MAIN CONSOLE - INITIATING AUCTION 2026")
    print(f"Server listening on port {PORT}...")
    print(f"Maximum connected users: {MAX_USERS}")

    while True:
        conn, addr = server.accept()

        # Confere clientes já registrados
        with client_lock:
            quant = len(clients)

        if quant >= MAX_USERS:
            conn.sendall(
                "ERROR -> LIMIT EXCEEDED.\n".encode("utf-8")
            )

            conn.close()

            logging.warning("Conexao recusada: limite de clientes atingido")

            continue
        # Iniciando Threading:
        parallel_user = threading.Thread(target=mult_client,args=(conn, addr),daemon=True)

        parallel_user.start()

        logging.info("THREAD CREATED FOR %s",addr)

if __name__ == "__main__":
    main()