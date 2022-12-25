import sqlite3


class DatabaseUtility:
    def __init__(self, _databaseName):
        self.name = _databaseName
        # Aprire la connessione a SQLite
        self.conn = sqlite3.connect(_databaseName)
        self.cursor = self.conn.cursor()
        if self.createMessageDatabaseIfNotExist():
            print("message database was not found. I create a new one")
        else:
            print("message database already exist")
        if self.createUserDatabaseIfNotExist():
            print("user database was not found. I create a new one")
        else:
            print("user database already exist")

        if self.createHashDatabaseIfNotExist():
            print("hash database was not found. I create a new one")
        else:
            print("hash database already exist")

    def createMessageDatabaseIfNotExist(self):
        """
        Crea una tabella per conservare tutti i messaggi se non esiste
        :return:
        """
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                sender TEXT NOT NULL,
                recipient TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                channel TEXT NOT NULL,
                private INTEGER NOT NULL
            )"""
        )
        self.conn.commit()

    def createUserDatabaseIfNotExist(self):
        """
        Crea una tabella per conservare tutti i messaggi se non esiste
        :return:
        """
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                nickName TEXT NOT NULL,
                mail TEXT NOT NULL,
                password TEXT NOT NULL,
                hashId TEXT NOT NULL,
                isKicked INTEGER NOT NULL,
                isBlackListed INTEGER NOT NULL
            )"""
        )
        self.conn.commit()

    def createHashDatabaseIfNotExist(self):
        """
        Crea una tabella per conservare tutti i messaggi se non esiste
        :return:
        """
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY,
                nickName TEXT NOT NULL,
                hashKey TEXT NOT NULL,
                AESKey TEXT NOT NULL,
                RSApublic TEXT NOT NULL,
                RSAprivate BOOL NOT NULL
            )"""
        )
        self.conn.commit()

    def createTable(self, _tableName, primaryKey, *args):
        creationString = f"CREATE TABLE {_tableName} ({primaryKey} INTEGER PRIMARY KEY, "
        for arg in args:
            creationString += f"{arg},"
        creationString[:-1] += ")"
        self.cursor.execute(creationString)

    def storeANewClient(self, client: 'clientObj'):
        _nickName = client.nickName
        _address = client.address
        self.cursor.execute(
            """INSERT INTO users (nickName, mail, password, address, hashId, isKicked, isBlackListed)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (client.nickName, client.mail,
             client.password, client.hashId,
             client.isKicked, client.isBlackListed)
        )
        self.conn.commit()

    def storeMessage(self, _message):
        self.cursor.execute(
            """INSERT INTO messages (timestamp, sender, msgType, recipient, message)
               VALUES (?, ?, ?, ?)""",
            (_message["timestamp"], _message["sender"], _message["msgType"], _message["recipient"], _message["message"])
        )
        self.conn.commit()

    def listMessageByNickName(self, _nickName):
        pass

    def printTable(self, _table):
        self.cursor.execute("SELECT * FROM users")
        results = self.cursor.fetchall()
        for result in results:
            print(result)

    def printColumName(self, tableName):
        # Eseguire la query PRAGMA table_info
        self.cursor.execute(f"PRAGMA table_info({tableName})")

        # Iterare sui risultati della query
        for column in self.cursor.fetchall():
            # Stampare il nome della colonna (il primo elemento della tupla restituita da PRAGMA table_info)
            print(column[1])

    def deleteATable(self, _table):
        pass

    def deleteAllTable(self):
        pass

    def __del__(self):
        # Chiudere la connessione a SQLite
        self.conn.close()
