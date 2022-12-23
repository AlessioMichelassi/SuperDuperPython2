"""

Ci sono diversi modi per creare un database in Python, a seconda delle tue esigenze e delle tue preferenze. Ecco
alcune opzioni comuni:

    SQLite: questo è probabilmente il modo più semplice per creare un database in Python. SQLite è un database
    leggero e incorporato che non richiede l'installazione di alcun software di terze parti. È possibile utilizzare
    il modulo sqlite3 di Python per connettersi a un database SQLite e creare tabelle, inserire dati, ecc.

Ecco un esempio di come creare una tabella e inserire alcuni dati in un database SQLite in Python:

"""

import sqlite3

# Connessione al database
conn = sqlite3.connect('database.db')

# Creazione del cursore
c = conn.cursor()

# Creazione della tabella
c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

# Inserimento dei dati
c.execute("INSERT INTO users (name, age) VALUES ('Alice', 25)")
c.execute("INSERT INTO users (name, age) VALUES ('Bob', 30)")

# Salvataggio delle modifiche
conn.commit()

# Chiusura della connessione
conn.close()

"""
MySQL: se hai bisogno di un database più potente e robusto, potresti considerare l'utilizzo di MySQL. Per 
utilizzare MySQL con Python, è necessario installare il modulo mysql-connector-python. Una volta installato, 
è possibile utilizzare il modulo per connettersi a un database MySQL e eseguire query SQL come in questo esempio: 
"""

import mysql.connector

# Connessione al database
conn = mysql.connector.connect(user='username', password='password', host='hostname', database='database_name')

# Creazione del cursore
cursor = conn.cursor()

# Creazione della tabella
cursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

# Inserimento dei dati
cursor.execute("INSERT INTO users (name, age) VALUES ('Alice', 25)")
cursor.execute("INSERT INTO users (name, age) VALUES ('Bob', 30)")

# Salvataggio delle modifiche
conn.commit()

# Chiusura della connessione
conn.close()


"""
Altri database: oltre a SQLite e MySQL, ci sono molti altri database che è possibile utilizzare con Python, 
come ad esempio PostgreSQL, MongoDB e altri ancora. Ognuno di questi database ha il proprio modulo Python che puoi 
utilizzare per connetterti e lavorare con esso. Ad esempio, per utilizzare PostgreSQL con Python, è possibile 
installare il modulo psycopg2 e utilizzarlo per connettersi e eseguire query al database come in questo esempio: 

"""

import psycopg2

# Connessione al database
conn = psycopg2.connect(host='hostname', database='database_name', user='username', password='password')

# Creazione del cursore
cursor = conn.cursor()

# Creazione della tabella
cursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

# Inserimento dei dati
cursor.execute("INSERT INTO users (name, age) VALUES ('Alice', 25)")
cursor.execute("INSERT INTO users (name, age) VALUES ('Bob', 30)")

# Salvataggio delle modifiche
conn.commit()

# Chiusura della connessione
conn.close()
