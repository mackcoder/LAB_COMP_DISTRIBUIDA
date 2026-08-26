# User da loja
# Naoto Ushizaki - 10437445 - 06G

import socket
import threading

PROPRIETARIO = "localhost"
PORT = 5000
Quant_c = 20

def mult_client(id):
    try:
        shop_c = socket.socket(socket.AF_INET,socket.SOCKET_STREAM)
        shop_c.connect(PROPRIETARIO, PORT)
        request = "COMPRAR"
        
        shop_c.sendall(request.encode("utf-8"))
        
        response = shop_c.recv(1024).decode('utf-8')
        print(f"[Cliente {id}] Resposta: {response}")
        
        shop_c.close()
    except:
        pass

    if __name__ == "__main__":
        threads = []
        print("Joined Loja!- Connection linked.")
        
        for _ in range(Quant_c):
            worker = threading.Thread(target = mult_client)
            worker = threads.append(worker)
            worker.start()
            
            for a in worker:
                worker.join()
                
        print("Todos os clientes finalizaram as requisicoes.")
