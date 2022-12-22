"""Il modulo multiprocessing di Python è un modulo che fornisce una interfaccia simile a quella dei thread per
eseguire attività in parallelo su più processi. I processi hanno il loro spazio di indirizzamento separato e non
condividono le risorse del sistema, il che li rende meno suscettibili ai problemi di sincronizzazione rispetto ai
thread. Tuttavia, la creazione e la gestione dei processi ha un overhead di performance maggiore rispetto ai thread.

Il modulo multiprocessing fornisce diverse funzionalità per la creazione e la gestione dei processi, come ad esempio
la classe Process per creare un processo, la classe Queue per creare una coda di comunicazione tra processi,
e la classe Lock per gestire l'accesso esclusivo alle risorse condivise.

La principale differenza tra il modulo multiprocessing e il modulo threading di Python è che il primo permette di
eseguire attività in parallelo su più processi, mentre il secondo permette di eseguire attività in parallelo su un
unico processo utilizzando i thread.

I processi hanno il loro spazio di indirizzamento separato e non condividono le risorse del sistema, il che li rende
meno suscettibili ai problemi di sincronizzazione rispetto ai thread. Tuttavia, la creazione e la gestione dei
processi ha un overhead di performance maggiore rispetto ai thread.

I thread, d'altra parte, condividono lo spazio di indirizzamento e le risorse del sistema con il processo principale,
il che li rende più facili da gestire ma più suscettibili ai problemi di sincronizzazione. Inoltre, il GIL (Global
Interpreter Lock) di Python limita l'esecuzione parallela dei thread, rendendo difficile ottenere un significativo
aumento delle prestazioni utilizzando i thread in Python.

L'overhead di performance è il costo aggiuntivo in termini di tempo o risorse che un'attività comporta rispetto
all'attività principale. Ad esempio, la creazione e la gestione dei processi ha un overhead di performance maggiore
rispetto all'esecuzione sequenziale del codice, poiché richiede tempo e risorse aggiuntive per la creazione e la
gestione dei processi stessi.

L'overhead di performance può essere causato da diverse cose, come ad esempio la creazione di strutture dati
aggiuntive, la gestione della memoria, la sincronizzazione tra thread o processi, o l'esecuzione di codice aggiuntivo
per la gestione delle attività parallele.

È importante considerare l'overhead di performance quando si valuta l'utilizzo di tecniche di parallellizzazione del
codice, poiché un overhead troppo elevato potrebbe annullare o addirittura peggiorare le prestazioni del programma.

Ecco alcuni esempi di come utilizzare il modulo multiprocessing per eseguire attività in parallelo su più processi in Python:

    Esempio di creazione di un processo:

"""

import multiprocessing


def process_function(name):
    print(f"Processo {name}: avviato")


# crea un processo
process = multiprocessing.Process(target=process_function, args=("Process 1",))

# avvia il processo
process.start()

# aspetta la terminazione del processo
process.join()

"""
Esempio di creazione di più processi:
"""

import multiprocessing


def process_function(name):
    print(f"Processo {name}: avviato")


processes = []
for i in range(4):
    process = multiprocessing.Process(target=process_function, args=(f"Process {i + 1}",))
    process.start()
    processes.append(process)

for process in processes:
    process.join()

print("Tutti i processi sono terminati")

"""
In questo caso, vengono creati 4 processi che eseguono in parallelo la funzione process_function.

Esempio di utilizzo di una coda di comunicazione tra processi:
"""

import multiprocessing


def process_function(queue):
    print("Processo: avviato")
    # mette un valore nella coda
    queue.put("Processo: messaggio inviato")


# crea una coda di comunicazione
queue = multiprocessing.Queue()

# crea un processo
process = multiprocessing.Process(target=process_function, args=(queue,))

# avvia il processo
process.start()

# aspetta la terminazione del processo
process.join()

# legge il valore dalla coda
message = queue.get()
print(message)

"""In questo caso, viene creato un processo che mette un valore nella coda di comunicazione, e il processo principale 
legge il valore dalla coda una volta che il processo è terminato. 

    Esempio di utilizzo di un lock per gestire l'accesso esclusivo alle risorse condivise:
"""

import multiprocessing


def process_function(lock, resource):
    print("Processo: avviato")
    # acquisisce il lock
    lock.acquire()
    # modifica la risorsa condivisa
    resource.value += 1
    # rilascia il lock
    lock.release()


# crea una risorsa condivisa
resource = multiprocessing.Value("i", 0)

# crea un lock
lock = multiprocessing.Lock()

# crea un processo
process = multiprocessing.Process(target=process_function, args=(lock, resource))

# avvia il processo
process.start()

# aspetta la terminazione del processo
process.join()

# stampa il valore della risorsa condivisa
print(f"Risorsa condivisa: {resource.value}")

"""
In questo caso, viene creato un processo che modifica una risorsa condivisa utilizzando un lock per gestire 
l'accesso esclusivo alla risorsa. Il processo principale stampa il valore della risorsa una volta che il processo è 
terminato.

Ecco alcuni esempi di situazioni in cui potrebbe essere più adeguato utilizzare i thread o i processi:

    Esempio di utilizzo dei thread:

    Quando si vuole eseguire attività in parallelo all'interno di un processo per utilizzare al meglio le risorse del 
    sistema. Ad esempio, se si vuole sfruttare il multi-core di una CPU, i thread possono essere utilizzati per 
    eseguire attività in parallelo sui core diversi. Quando si vuole eseguire attività che richiedono una 
    sincronizzazione fine-grained, come ad esempio l'accesso a una risorsa condivisa. I thread possono utilizzare i 
    meccanismi di sincronizzazione forniti dal modulo threading, come i lock, per gestire l'accesso alle risorse 
    condivise. 

    Esempio di utilizzo dei processi:

    Quando si vuole eseguire attività in parallelo su più processi per sfruttare al meglio le risorse del sistema. Ad 
    esempio, se si vuole utilizzare più core di una CPU o più macchine, i processi possono essere utilizzati per 
    eseguire attività in parallelo su più processori o macchine. Quando si vuole evitare i problemi di 
    sincronizzazione legati all'accesso alle risorse condivise. I processi hanno il loro spazio di indirizzamento 
    separato e non condividono le risorse del sistema, il che li rende meno suscettibili ai problemi di 
    sincronizzazione rispetto ai thread. 

Spero che questi esempi ti siano stati utili! Se hai altre domande o vuoi saperne di più, non esitare a chiedere.
"""