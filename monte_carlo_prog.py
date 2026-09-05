from mpi4py import MPI

import random 
import time 

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
N = 10000000 

points_per_process = N // size

local_count = 0 
inicio = time.time() 

for _ in range(points_per_process): 
    x = random.random() 
    y = random.random() 
    if x*x + y*y <= 1: 
        local_count += 1 

# Junta as somas e as contagens locais de todos os processos no rank 0
total_final = comm.reduce(local_count, op=MPI.SUM, root=0)

# Agora no processo 0:
if rank == 0:
    total_points = points_per_process * size
    pi_estimated = 4 * local_count / total_points
    end = time.time()
    print("PI aproximado:", pi_estimated)
    print("Tempo distribuído (MPI):", (end - inicio) * 1000, "ms")

MPI.Finalize()