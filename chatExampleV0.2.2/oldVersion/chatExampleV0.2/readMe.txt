Chat Server/Client

Questo è un semplice server/chat di chat realizzato in Python. Il server può gestire più connessioni client
contemporaneamente e permette ai client di inviare messaggi tra loro e di ricevere messaggi dal server.

Il codice è stato creato da me usando l'ai come aiuto per tutte le cose che non sapevo.
Sperando possa essere di aiuto a qualcuno lo rilasci con licenza MIT.

https://chat.openai.com/


Come funziona

Il server utilizza il protocollo TCP per le connessioni e utilizza il modulo threading di Python per gestire
le connessioni client in modo asincrono. Ogni connessione client viene gestita da un thread separato,
che si occupa di ricevere e inviare i messaggi del client.

Il server include anche alcune funzionalità di base per fare entrare come root e bannare gli utenti indisciplinati;
oltre a questo ha un procedimento di handshake per il primo collegamento e l'inserimento del nick name.

i messaggi inviati dal client vengono creati utilizzando jSon. Per poterli inviare/ricevere correttamente
viene inviata prima la stringa contenente la dimensione del messaggio e quindi il messaggio json.
Ogni messaggio inviato o ricevuto dal server o dai client contiene un header di 10 caratteri
che indica la lunghezza del messaggio seguito dal messaggio stesso in formato JSON.
Ad esempio, un messaggio potrebbe avere questa struttura:

primoMessaggio = '0000000010'
secondoMessaggio = {"sender": "Server",
                    "date": "2022-12-20 12:34:56",
                    "message": "Benvenuto nel server di chat"}'


Utilizzo

Per utilizzare il server, è sufficiente eseguire il file server.py.
Il server utilizzerà l'indirizzo IP locale e la porta specificati come argomenti di default,
ma è possibile modificarli inserendo i valori desiderati nei costanti HOST_IP e HOST_PORT.

Per connettersi al server, è sufficiente utilizzare un client TCP qualsiasi, ad esempio il comando
telnet da linea di comando o un'applicazione client personalizzata.

Una volta connesso, è possibile inviare messaggi digitando il testo desiderato e premendo il tasto invio.
Il server visualizzerà i messaggi ricevuti e li invierà a tutti gli altri client connessi.


Comandi del server

Il server supporta alcuni comandi speciali,
che possono essere utilizzati iniziando il messaggio con il carattere '/':

    /nick <nuovo_nickname>: cambia il nickname dell'utente
    /kick <nickname>: disconnette un utente dal server
    /help: visualizza un elenco dei comandi disponibili
    /root: per entrare nel server in modalità amministratore
    /list: per avere una lista degli utenti nella chat
    /msg: per mandare un messaggio privato a un certo client senza che lo veda tutta la chat

Struttura del codice

Il codice del server è strutturato in tre classi principali:

    ServerX: questa classe rappresenta il server e gestisce le connessioni client,
    l'invio e la ricezione dei messaggi e la gestione dei comandi. Inoltre, gestisce le
    connessioni dei nuovi client.

    clientObj: questa classe rappresenta un client connesso al server e contiene informazioni
    sulla connessione del client, come il nickname, il socket e l'indirizzo IP.

    ClientThread: rappresenta un thread dedicato ad un singolo client.
    Ogni volta che un nuovo client si connette al server, viene creato un nuovo thread
    che si occupa di gestire le richieste e i messaggi inviati dal client.

Funzionamento

Quando il server viene avviato, entra in ascolto di richieste di connessione sulla porta specificata.

Quando un nuovo client si connette, viene creato un nuovo oggetto clientObj che rappresenta il client
appena connesso. A questo punto, viene creato un nuovo thread dedicato al client,
che si occupa di gestire le richieste e i messaggi inviati dal client stesso. I messaggi che contengono
solo testo vengono deviati verso tutti gli altri client, mentre i messaggi che invece contengono un comando
vengono gestiti dalla funzione handleMessage.