# Siste. Vendas
# Naoto Ushizaki - 10437445 - 06G

import socket
import threading

PROPRIETARIO = "localhost"
PORT = 5000
num_clients = 10

estoque = 10
cadeado = threading.Lock()

def client_system(connection):
    global estoque
    
    while True:
        message = connection.recv(1024).decode
        
        if not message:
            break
            
        if message.upper() == "COMPRAR":
            if estoque == 0:
                print("ERROR - Esgotado")
            else:
                with cadeado:
                    estoque -= 1
                    response = f"Transaction complete! Estoque left: {estoque}"
        if message.upper() == "CONSULTAR":
            print("QUANT: %d", estoque)

        if estoque == 0:
            connection.sendall("Produto esgotado. Volte mais tarde")
            break
        connection.send(response.encode())
    connection.close()
    
machine_spirit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
machine_spirit.bind("localhost", 5000)
machine_spirit.listen()
print("Vox Transmission connected...")

while True:
    connection, addr = machine_spirit.accept()
    threading.thread(target = client_system, args = (connection, )).start()
    



