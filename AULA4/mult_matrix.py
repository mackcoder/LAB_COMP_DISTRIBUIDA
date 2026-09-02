from mpi4py import MPI
import time
import random
import threading

NUM = 300
WORKERS = 4

A = [[random.random() for _ in range(NUM)] for _ in range(NUM)]
B = [[random.random() for _ in range(NUM)] for _ in range(NUM)]
C = [[0]*NUM for _ in range(NUM)]

def calcular(inicio, fim):
    for i in range(inicio, fim):
        for j in range(NUM):
            for k in range(NUM):
             C[i][j] += A[i][k] * B[k][j]

start = time.time()
workers = []
lines = NUM // WORKERS

for t in range(WORKERS):
    ini = t * lines
    fim = NUM if t == WORKERS-1 else (t+1)*workers
    th = threading.Thread(target=calcular, args=(ini, fim))
    workers.append(th)
    th.start()
    for th in workers:
        th.join()
    fim = time.time()
    print("Tempo com threads:", (fim-start)*1000, "ms")

fim = time.time()
print("Tempo com threads:", (fim-start)*1000, "ms")
