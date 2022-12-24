"""
In Python, i thread sono un modo per eseguire più codice allo stesso tempo in un processo.
Possono essere utilizzati per sfruttare al meglio le risorse hardware del computer,
ad esempio eseguendo operazioni in parallelo su più core o processori.

Per utilizzare i thread in Python, è prima necessario importare il modulo threading.
Una volta fatto ciò, è possibile creare un nuovo thread eseguendo il codice che
si desidera eseguire in parallelo all'interno di una classe che erediti da threading.Thread.

Ad esempio:
"""

import threading


class MyThread(threading.Thread):
    def run(self):
        # codice da eseguire in parallelo va inserito qui
        print("Hello from a thread!")


thread = MyThread()
thread.start()

"""
La classe threading.Thread ha diverse opzioni di configurazione, come il nome del thread e se il thread deve essere 
avviato come daemon (un thread daemon viene interrotto quando il processo principale termina). 
È anche possibile utilizzare il metodo join per bloccare l'esecuzione del processo principale 
fino a quando il thread non è terminato.

Ecco un esempio completo che utilizza i thread per stampare i numeri da 1 a 10 in parallelo:
"""

import threading


class PrintThread(threading.Thread):
    def __init__(self, start, end):
        super().__init__()
        self.start = start
        self.end = end

    def run(self):
        for i in range(self.start, self.end):
            print(i)


thread1 = PrintThread(1, 6)
thread2 = PrintThread(6, 11)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

"""
DAEMON THREAD
Un daemon thread è un thread che viene eseguito in background e che viene interrotto automaticamente quando il 
processo principale termina. In altre parole, un daemon thread è un thread che viene utilizzato per eseguire attività 
di supporto in background, senza interferire con l'esecuzione del processo principale. 

In Python, è possibile creare un daemon thread impostando il flag daemon su True quando si crea il thread. Ad esempio:
"""

import threading


def my_function():
    # codice da eseguire in parallelo va inserito qui
    print("Hello from a daemon thread!")


thread = threading.Thread(target=my_function, daemon=True)
thread.start()

"""
È importante notare che, poiché i daemon thread vengono interrotti automaticamente quando il processo principale 
termina, non è possibile utilizzare il metodo join per attendere la loro completazione. Inoltre, i daemon thread non 
devono avere alcun lavoro importante da eseguire al termine del processo principale, poiché possono essere interrotti 
in qualsiasi momento. 

Ci sono diverse opzioni per fermare un thread in Python. Ecco alcune delle principali:

    Usare il metodo thread.join(): questo metodo bloccherà l'esecuzione del processo principale fino a quando il 
    thread non è terminato. Tuttavia, questo metodo può essere utilizzato solo per attendere la completazione del 
    thread e non può essere utilizzato per interrompere il thread prima del suo termine. 

    Usare una variabile di controllo: è possibile utilizzare una variabile di controllo per indicare al thread quando 
    deve terminare. Ad esempio, si potrebbe definire una variabile booleana stop_thread e impostarla su True quando 
    si vuole interrompere il thread. Il thread dovrebbe quindi controllare periodicamente questa variabile e uscire 
    dal suo ciclo di esecuzione quando viene impostata su True. 

    Usare il metodo thread.raise_exception(): questo metodo permette di sollevare un'eccezione nel thread, 
    interrompendone l'esecuzione. Tuttavia, questo metodo può essere utilizzato solo se il thread ha un gestore di 
    eccezioni che può gestire l'eccezione sollevata. 

    Usare il metodo thread.stop(): questo metodo interrompe il thread, tuttavia è deprecato dalla versione 3.4 di 
    Python in poi e non dovrebbe essere utilizzato. 

In generale, la migliore opzione per interrompere un thread dipende dalle esigenze specifiche del tuo codice.

Ecco alcuni esempi di codice che mostrano come fermare un thread in Python utilizzando i 
diversi metodi descritti in precedenza:

    Usare il metodo thread.join():
"""

import threading
import time


def my_function():
    while True:
        print("Hello from a thread!")
        time.sleep(1)


thread = threading.Thread(target=my_function)
thread.start()

# attendi che il thread finisca
thread.join()

#
#
# Usare una variabile di controllo:

import threading
import time


def my_function(stopThread):
    while not stopThread:
        print("Hello from a thread!")
        time.sleep(1)


stop_thread = False
thread = threading.Thread(target=my_function, args=(stop_thread,))
thread.start()

# interrompi il thread dopo 5 secondi
time.sleep(5)
stop_thread = True
thread.join()

#
#
# Usare il metodo thread.raise_exception():

import threading


def my_function():
    try:
        while True:
            print("Hello from a thread!")
    except Exception as e:
        print("Thread interrupted")


thread = threading.Thread(target=my_function)
thread.start()

# interrompi il thread sollevando un'eccezione
thread.raise_exc(Exception)
thread.join()

"""
ci sono diversi modi per gestire più thread contemporaneamente in Python. Ecco alcune delle opzioni più comuni:

    Usare il metodo threading.Thread.join(): questo metodo può essere utilizzato per attendere la completazione di un 
    thread specifico. Ad esempio, per attendere la completazione di due thread thread1 e thread2, si potrebbe 
    scrivere: """

thread1.join()
thread2.join()

"""
Usare il modulo threading.Event: questo modulo offre un oggetto evento che può essere utilizzato per sincronizzare 
l'esecuzione di più thread. Ad esempio, si può creare un evento e e far aspettare i thread fino a quando l'evento non 
viene impostato: 
"""

import threading

e = threading.Event()


def my_function():
    e.wait()
    # codice da eseguire quando l'evento viene impostato va inserito qui


thread1 = threading.Thread(target=my_function)
thread2 = threading.Thread(target=my_function)

thread1.start()
thread2.start()

# fai aspettare i thread fino a quando l'evento non viene impostato
e.set()

thread1.join()
thread2.join()

"""
Usare il modulo threading.Semaphore: questo modulo offre un oggetto semaforo che può essere utilizzato per 
limitare l'accesso di un certo numero di thread a una risorsa condivisa. Ad esempio, si può creare un semaforo s con 
un valore di 3 e far aspettare i thread fino a quando il semaforo non è disponibile: 

"""

import threading

s = threading.Semaphore(3)


def my_function():
    s.acquire()
    a = 0
    try:
        # codice da eseguire con l'accesso alla risorsa va inserito qui
        a += 1
    finally:
        s.release()


thread1 = threading.Thread(target=my_function)
thread2 = threading.Thread(target=my_function)
thread3 = threading.Thread(target=my_function)
thread4 = threading.Thread(target=my_function)

thread1.start()
thread2.start()
thread3.start()
thread4.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()

"""
Un thread pool è un insieme di thread prealloccati che possono essere riutilizzati per eseguire diverse attività. 
Un thread pool può essere utilizzato per eseguire più attività in parallelo, senza dover creare e distruggere nuovi 
thread ogni volta. Ciò può ridurre il overhead di creazione dei thread e aumentare l'efficienza del programma.

In Python, è possibile utilizzare il modulo concurrent.futures per creare un thread pool. Ad esempio, si può 
creare un thread pool con 4 thread eseguendo il seguente codice:
"""

import concurrent.futures

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    # codice da eseguire con il thread pool va inserito qui
    pass

"""
Una volta creato il thread pool, è possibile utilizzare il metodo submit per inviare una funzione da eseguire 
in uno dei thread del pool. Ad esempio:
"""

import concurrent.futures


def my_function(x):
    return x * x


with concurrent.futures.ThreadPoolExecutor(max_workers=4) as _executor:
    result = _executor.submit(my_function, 10)
    print(result.result())  # stampa 100

"""
È anche possibile inviare più funzioni contemporaneamente al thread pool e ottenere i risultati in modo 
asincrono utilizzando il metodo map:
"""

import concurrent.futures


def my_function(x):
    return x * x


with concurrent.futures.ThreadPoolExecutor(max_workers=4) as _executor:
    results = _executor.map(my_function, [1, 2, 3, 4])
    for result in results:
        print(result)  # stampa 1, 4, 9, 16
