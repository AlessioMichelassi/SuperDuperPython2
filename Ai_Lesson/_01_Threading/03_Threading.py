"""
Ci sono alcune altre cose che vale la pena menzionare quando si parla di thread in Python:

    Thread local storage: il modulo threading fornisce la classe local che permette di creare variabili locali ai
    thread. Ciò significa che ogni thread può avere il suo valore per la variabile, indipendentemente dal valore
    delle altre istanze della stessa variabile in altri thread.

    Thread-safe functions: alcune funzioni di Python, come ad esempio print o time.sleep, sono thread-safe,
    ovvero possono essere utilizzate in modo sicuro da più thread senza causare problemi di sincronizzazione. Altre
    funzioni, come ad esempio list.append, non sono thread-safe e potrebbero causare problemi di sincronizzazione se
    utilizzate da più thread contemporaneamente.

    Multiprocessing: in Python, è possibile utilizzare anche il modulo multiprocessing per eseguire attività in
    parallelo su più processi. A differenza dei thread, i processi hanno il loro spazio di indirizzamento separato e
    non condividono le risorse del sistema, il che li rende meno suscettibili ai problemi di sincronizzazione.
    Tuttavia, la creazione e la gestione dei processi ha un overhead di performance maggiore rispetto ai thread.


 Ecco alcuni esempi di come utilizzare la classe local e le funzioni thread-safe in Python:

    Esempio di thread local storage:
"""

import threading

# crea una variabile thread local
local_data = threading.local()


def thread_function(name):
    # imposta un valore per la variabile thread local
    local_data.name = name
    print(f"Thread {local_data.name}: impostato nome")


thread1 = threading.Thread(target=thread_function, args=("Thread 1",))
thread2 = threading.Thread(target=thread_function, args=("Thread 2",))

thread1.start()
thread2.start()

thread1.join()
thread2.join()

"""
In questo caso, ogni thread ha il suo valore per la variabile local_data.name, indipendentemente dal valore delle 
altre istanze della stessa variabile in altri thread. 

    Esempio di funzioni thread-safe:
"""

import threading
import time


# la funzione print è thread-safe
def thread_function(name):
    print(f"Thread {name}: avviato")
    time.sleep(1)  # la funzione time.sleep è thread-safe
    print(f"Thread {name}: terminato")


thread1 = threading.Thread(target=thread_function, args=("Thread 1",))
thread2 = threading.Thread(target=thread_function, args=("Thread 2",))

thread1.start()
thread2.start()

thread1.join()
thread2.join()


"""
In questo caso, le funzioni print e time.sleep possono essere utilizzate in modo sicuro da più thread senza 
causare problemi di sincronizzazione. 

"""