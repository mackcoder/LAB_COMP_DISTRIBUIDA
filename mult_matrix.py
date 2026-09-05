from mpi4py import MPI

import time
import random

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

NUM = 1000
WORKERS = 4

if rank == 0:
    A = [[random.random() for _ in range(NUM)] for _ in range(NUM)]
    B = [[random.random() for _ in range(NUM)] for _ in range(NUM)]
else:
    A = None
    B = None

# Comeca contar tempo
inicio = time.time()

# Broadcast aqui:
A = comm.bcast(A, root = 0)
B = comm.bcast(B, root = 0)

lines_por_processo = NUM // size
ini = rank * lines_por_processo
fim = NUM if rank == size - 1 else (rank + 1) * lines_por_processo
 
C_local = []

# operacao principal:
for i in range(ini, fim):
    linha = [0] * NUM
    for j in range(NUM):
        soma = 0
        for k in range(NUM):
            soma += A[i][k] * B[k][j]
        linha[j] = soma
    C_local.append(linha)

# mandar para matrix C
C_partes = comm.gather(C_local, root=0)

if rank == 0:
    C = []
    for parte in C_partes:
        C.extend(parte)
 
    fim_tempo = time.time()
    # 6. Exibe o tempo de execução em milissegundos
    print("Tempo distribuído (MPI):", (fim_tempo - inicio) * 1000, "ms")