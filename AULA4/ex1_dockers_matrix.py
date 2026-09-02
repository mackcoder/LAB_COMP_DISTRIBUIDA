from mpi4py import MPI
import time
import random

NUM = 300
WORKERS = 4
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

lines_per_processing = NUM // size
start = rank * lines_per_processing
end = (rank + 1) * lines_per_processing if rank != size -1 else NUM

# Rank 0 criando as matrizes:
if rank == 0:
    A = [[random.random() for _ in range(NUM)] for _ in range(NUM)]
    B = [[random.random() for _ in range(NUM)] for _ in range(NUM)]
    start = start.time()

else:
   A = None
   B = None

# Mandando o Broadcast
B = comm.bcast(B, root = 0)

# Separar fatias das linhas A:
if rank == 0:
    piece1 = A[start:end]

    for a in range (1, size):
        p1_start = a * lines_per_processing
        p1_end = (a + 1) * lines_per_processing if a!=size - 1 else NUM
        comm.send(A[p1_start:p1_end], dest=a, tag = 1)
else:
    piece1 = comm.recv(source = 0, tag = 1)

start = time.time()

fatia_A = piece1

fatia_C = [[0.0] * NUM for _ in range(len(fatia_A))]

for i in range(len(fatia_A)):
    for j in range(NUM):
        soma = 0.0
        for k in range(NUM):
            soma += fatia_A[i][k] * B[k][j]
        fatia_C[i][j] = soma

total = comm.gather(fatia_C, root = 0)

if rank == 0:
    C = []
    for piece in total:
        C.extend(piece)

    fim_tempo = time.time()
    print("Tempo total de execução distribuída:", (fim_tempo - start) * 1000, "ms")
