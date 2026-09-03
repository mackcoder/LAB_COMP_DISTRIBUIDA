from mpi4py import MPI
import time
import random

# Naoto Ushizaki - 10437445

NUM = 300
WORKERS = 4
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

lines_per_processing = NUM // size
start = rank * lines_per_processing
end = (rank + 1) * lines_per_processing if rank != size -1 else NUM
rest = NUM % size
# Rank 0 criando as matrizes:
if rank == 0:
    A = [[random.random() for _ in range(NUM)] for _ in range(NUM)]
    B = [[random.random() for _ in range(NUM)] for _ in range(NUM)]

else:
   A = None
   B = None

# Mandando o Broadcast
A = comm.bcast(A, root = 0)
B = comm.bcast(B, root = 0)

# parte feita pela IA por estar dando problema:
if rank < rest:
    inicio = rank * (lines_per_processing + 1)
    fim = inicio + lines_per_processing + 1
else:
    inicio = rank * lines_per_processing + rest
    fim = inicio + lines_per_processing
#----------------------------------------------#
start = time.time()
fatia_C = []

for i in range(inicio, fim):
    line = [0.0]* NUM
    for j in range(NUM):
        soma = 0.0
        for k in range(NUM):
            soma += A[i][k] * B[k][j]
        line[j] = soma
    fatia_C.append(line)

total = comm.gather(fatia_C, root = 0)

if rank == 0:
    C = []
    for piece in total:
        C.extend(piece)

    fim_tempo = time.time()
    print("Tempo total de execução distribuída:", (fim_tempo - start) * 1000, "ms")
