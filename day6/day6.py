import threading
import multiprocessing
from queue import Queue
import time
from decimal import Decimal
from decimal import getcontext
import math

def euler_number_ps(start_term: int, end_term: int, que=None) -> Decimal:
    getcontext().prec = 100
    partial_sum = Decimal(0)
    for i in range(start_term, end_term):
        term = Decimal(1) / Decimal(math.factorial(i))
        partial_sum += term
    if que is not None:
        que.put(partial_sum)
    else:
        return partial_sum

def worker(start_index, end_index):
    return euler_number_ps(start_index, end_index)

if __name__ == "__main__":
    start_time = time.time()

    N = 1000  # Number of terms per process
    process_count = 8  # Number of processes

    num_cores = multiprocessing.cpu_count()
    print(f"Number of cores: {num_cores}")

    # Create the pool of workers
    pool = multiprocessing.Pool(processes=process_count)

    # Prepare ranges for the terms each process will handle
    tasks = [(N * i, N * (i + 1)) for i in range(process_count)]
    
    # Start the processes and collect results
    results = pool.starmap(worker, tasks)

    # Close the pool and wait for all workers to finish
    pool.close()
    pool.join()

    end_time = time.time()
    print(f"Multiprocessing finished: {end_time - start_time} seconds")

    # Combine the results from all processes
    result = sum(results)

    print(f"Result = {result}")

if 0:

    start_time = time.time()

    qres = Queue()

    N = 1000  # Number of terms per thread
    thread_count = 8  # Number of threads

    num_cores = multiprocessing.cpu_count()
    print(f"Number of core: {num_cores}")

    # Create and start threads
    thread_list = []
    for i in range(thread_count):
        start_index = N * i
        end_index = N * (i + 1)  # This makes sure each thread handles a range of terms
        t = threading.Thread(target=euler_number_ps, args=(start_index, end_index, qres))
        thread_list.append(t)
        t.start()
        print(f"Thread {i} started processing terms {str(start_index).rjust(15)} to {str(end_index - 1).rjust(15)}.")

    # Wait for all threads to complete
    for t in thread_list:
        t.join()

    end_time = time.time()
    print(f"Threading finished: {end_time - start_time} seconds")

    # Combine the results from all threads
    result = Decimal(0)
    while not qres.empty():
        result += qres.get()

    print(f"Result = {result}")
