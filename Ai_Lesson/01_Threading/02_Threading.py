"""
Ci sono diverse cose da sapere sui thread in Python, ecco alcune delle principali:

    Gestione della sincronizzazione: i thread possono condividere le risorse del sistema, come le variabili globali o
    le strutture dati condivise, e questo può portare a problemi di sincronizzazione. Ad esempio, due thread
    potrebbero modificare la stessa variabile contemporaneamente, causando risultati imprevedibili. Per evitare
    questi problemi, è possibile utilizzare i meccanismi di sincronizzazione forniti dal modulo threading,
    come i lock o i semafori.

    Deadlock: un deadlock si verifica quando due o più thread si bloccato in attesa di una risorsa che non verrà mai
    rilasciata, causando un blocco del programma. Per evitare i deadlock, è importante utilizzare i meccanismi di
    sincronizzazione in modo corretto e gestire attentamente l'accesso alle risorse condivise.

    GIL (Global Interpreter Lock): Python utilizza una feature chiamata GIL (Global Interpreter Lock) che limita
    l'esecuzione di un solo thread alla volta. Ciò significa che, anche se si utilizzano i thread per eseguire più
    attività in parallelo, solo uno di essi può effettivamente eseguire del codice Python alla volta. Tuttavia,
    il GIL non influisce sull'esecuzione di attività I/O o di calcolo pesante eseguite in moduli scritti in C,
    che possono quindi essere eseguite in parallelo ai thread Python.

    Performance: i thread possono essere utilizzati per migliorare le prestazioni del programma eseguendo attività in
    parallelo, ma devono essere utilizzati con attenzione poiché la gestione dei thread può avere un overhead di
    performance. Inoltre, come menzionato in precedenza, il GIL di Python limita l'esecuzione di un solo thread alla
    volta, quindi in alcuni casi l'utilizzo dei thread potrebbe non portare a un aumento delle prestazioni.


Ecco alcuni esempi di problemi comuni che possono verificarsi quando si utilizzano i thread in Python:

    Problemi di sincronizzazione:
"""

import threading

# una variabile globale condivisa da due thread
counter = 0


def increment_counter():
    global counter
    for i in range(10000):
        counter += 1


def decrement_counter():
    global counter
    for i in range(10000):
        counter -= 1


thread1 = threading.Thread(target=increment_counter)
thread2 = threading.Thread(target=decrement_counter)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print(counter)  # il risultato potrebbe essere imprevedibile

"""
In questo caso, i due thread modificano la variabile globale counter contemporaneamente, causando risultati 
imprevedibili. Per evitare questo problema, è possibile utilizzare un lock per garantire l'accesso esclusivo alla 
variabile: 

"""

import threading

# una variabile globale condivisa da due thread
counter = 0
lock = threading.Lock()


def increment_counter():
    global counter
    with lock:
        for i in range(10000):
            counter += 1


def decrement_counter():
    global counter
    with lock:
        for i in range(10000):
            counter -= 1


thread1 = threading.Thread(target=increment_counter)
thread2 = threading.Thread(target=decrement_counter)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print(counter)  # il risultato dovrebbe essere 0

"""
Deadlock:
"""
import threading

lock1 = threading.Lock()
lock2 = threading.Lock()


def thread1_function():
    with lock1:
        print("Thread 1: acquisito lock 1")
        with lock2:
            print("Thread 1: acquisito lock 2")


def thread2_function():
    with lock2:
        print("Thread 2: acquisito lock 2")
        with lock1:
            print("Thread 2: acquisito lock 1")


thread1 = threading.Thread(target=thread1_function)
thread2 = threading.Thread(target=thread2_function)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

"""
In questo caso, i due thread cercano di acquisire i lock in ordine inverso, causando un deadlock. Per evitare 
questo problema, è importante utilizzare sempre i lock in modo coerente e fare attenzione all'ordine in cui vengono 
acquisiti. 


Esempio di GIL:
"""

import threading
import time


def thread_function():
    print("Thread avviato")
    time.sleep(5)
    print("Thread terminato")


threads = []
for i in range(4):
    thread = threading.Thread(target=thread_function)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print("Tutti i thread sono terminati")

"""
In questo caso, anche se sono stati avviati 4 thread, solo uno di essi può eseguire del codice Python alla volta a 
causa del GIL. Ciò significa che i thread eseguiranno il codice a turno, senza eseguirlo in parallelo. 

    Esempio di performance:
"""

import threading
import time


def thread_function(n):
    start = time.perf_counter()
    for i in range(n):
        x = i ** 2
    end = time.perf_counter()
    print(f"Tempo impiegato: {end - start:.6f} secondi")


threads = []
for i in range(4):
    thread = threading.Thread(target=thread_function, args=(10000000,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print("Tutti i thread sono terminati")

"""In questo caso, anche se sono stati avviati 4 thread, solo uno di essi può eseguire del codice Python alla volta a 
causa del GIL. Ciò significa che l'esecuzione dei thread non porterà a un aumento delle prestazioni rispetto 
all'esecuzione sequenziale del codice. """
