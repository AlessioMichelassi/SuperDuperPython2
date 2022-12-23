"""MySQL e SQLite sono entrambi database relazionali, il che significa che utilizzano una struttura di tabelle per
archiviare i dati. Tuttavia, ci sono alcune importanti differenze tra i due:

    Server o incorporato: MySQL è un database server, il che significa che deve essere installato su un server e che
    gli utenti possono connettersi ad esso da remoto per eseguire query e gestire il database. SQLite, d'altra parte,
    è un database incorporato, il che significa che viene incorporato direttamente all'interno dell'applicazione che
    lo utilizza. Non è necessario installare un server separato per utilizzare SQLite.

    Scalabilità: MySQL è progettato per gestire grandi quantità di dati e molti utenti contemporaneamente,
    il che lo rende adatto per le applicazioni di grandi dimensioni e ad alto traffico. SQLite, d'altra parte,
    è più adatto per le applicazioni di piccole e medie dimensioni, poiché non è progettato per gestire carichi di
    lavoro pesanti.

    Facilità d'uso: SQLite è probabilmente più facile da utilizzare rispetto a MySQL, poiché non richiede
    l'installazione di un server separato e ha una sintassi SQL più semplice. MySQL, d'altra parte, richiede un po'
    più di configurazione e può essere più complesso da utilizzare per gli utenti meno esperti.

In generale, MySQL è una scelta migliore per le applicazioni di grandi dimensioni che hanno bisogno di un database
potente e scalabile, mentre SQLite è una buona opzione per le applicazioni di piccole e medie dimensioni che hanno
bisogno di un database semplice e leggero. SQLite è un database leggero e incorporato che è molto facile da usare con
Python.

Un database relazionale è un tipo di database che utilizza una struttura di tabelle per archiviare i dati. Ogni
tabella rappresenta una "relazione" tra diverse entità, ad esempio gli utenti di un'applicazione o gli articoli in un
negozio online.

Le tabelle di un database relazionale sono composte da righe (chiamate "record") e colonne (chiamate "campi"). Ogni
riga rappresenta un'entità specifica, ad esempio un utente specifico o un articolo specifico, mentre ogni colonna
rappresenta una caratteristica di quell'entità, ad esempio il nome di un utente o il prezzo di un articolo.

Le tabelle di un database relazionale sono spesso correlate tra loro mediante chiavi esterne. Una chiave esterna è un
campo che fa riferimento a una chiave primaria (un campo univoco) in un'altra tabella. Ad esempio, una tabella degli
ordini potrebbe fare riferimento alla chiave primaria di una tabella degli utenti per indicare l'utente che ha
effettuato l'ordine.

I database relazionali sono molto diffusi e vengono utilizzati in molti tipi di applicazioni, come ad esempio negozi
online, social network e sistemi di gestione dei contenuti. MySQL, SQLite e PostgreSQL sono tutti esempi di database
relazionali.Tuttavia, esistono anche altri tipi di database, come ad esempio i database NoSQL, che utilizzano una
struttura di dati diversa da quella delle tabelle.

I database NoSQL sono progettati per gestire grandi quantità di dati non strutturati e sono spesso utilizzati in
applicazioni che richiedono una scalabilità orizzontale (cioè la possibilità di aggiungere facilmente nuovi server
per gestire un carico di lavoro crescente). MongoDB, Cassandra e Couchbase sono tutti esempi di database NoSQL.

Spero che questo ti aiuti a capire la differenza tra database relazionali e NoSQL. Se hai bisogno di ulteriore
assistenza o se hai altre domande, non esitare a chiedere.

Ecco alcuni passaggi per iniziare a utilizzare SQLite con Python:

    nel caso non sia presente, installa il modulo sqlite3 di Python: può essere fatto utilizzando pip,
    il gestore di pacchetti di Python. Apri il terminale e digita il seguente comando per installare il modulo:

    pip install sqlite3

Crea una connessione al database: per lavorare con un database SQLite, dovrai prima connetterti ad esso. Questo può
essere fatto utilizzando il metodo connect del modulo sqlite3. Ecco un esempio di come connettersi ad un database
chiamato "database.db":

"""

import sqlite3

conn = sqlite3.connect('database.db')

"""
Crea un cursore: una volta che ti sei connesso al database, dovrai creare un cursore per eseguire query e 
modificare il database. Un cursore è un oggetto che ti permette di eseguire operazioni sul database. 
Ecco come creare un cursore: 
"""

cursor = conn.cursor()

"""
Esegui query SQL: ora che hai un cursore, puoi eseguire query SQL per creare tabelle, 
inserire dati, ecc. Ecco un esempio di come creare una tabella e inserire alcuni dati nel database:
"""

# Creazione della tabella
cursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

# Inserimento dei dati
cursor.execute("INSERT INTO users (name, age) VALUES ('Alice', 25)")
cursor.execute("INSERT INTO users (name, age) VALUES ('Bob', 30)")

"""
Salva le modifiche: ogni volta che modifichi il database, 
dovrai salvare le modifiche utilizzando il metodo commit della connessione. 
Ecco come fare:
"""

conn.commit()

"""
Chiudi la connessione: infine, non dimenticare di chiudere la connessione al database 
quando hai finito di lavorare con esso. Ecco come chiudere la connessione:
"""

conn.close()
