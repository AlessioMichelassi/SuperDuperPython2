"""
Per creare una classe utility per gestire le operazioni di database in SQLite, puoi seguire i seguenti passaggi:

    Includere le librerie necessarie per la connessione a SQLite. In PHP, puoi utilizzare la libreria PDO per
    la connessione a SQLite.

    Creare una classe per la tua utility di database, con metodi per gestire le operazioni di database
    di cui hai bisogno. Ad esempio, puoi creare un metodo per creare un database, un metodo per cancellare
    un database e un metodo per copiare un database.

    In ogni metodo, aprire una connessione a SQLite e utilizzare le query SQL appropriate per eseguire l'operazione
    di database richiesta. Ad esempio, per creare un database, puoi utilizzare la query CREATE DATABASE nome_database
    (che non è supportata in SQLite); per cancellare un database, puoi utilizzare la query DROP DATABASE nome_database
    (che non è supportata in SQLite); per copiare un database, puoi utilizzare
    la query CREATE TABLE nuovo_nome_database AS SELECT * FROM vecchio_nome_database.

    Chiudere la connessione a SQLite quando hai finito di utilizzare la tua utility di database.

Ecco un esempio di come potrebbe essere strutturata la tua classe utility di database in PHP utilizzando SQLite:
"""

import sqlite3
import json
import threading
import socket
import time

from Ai_Lesson._02_Cryptography.cryptoFunction import cryptex

# Define socket constants to be used
hostName = socket.gethostname()
HOST_IP = socket.gethostbyname(hostName)
HOST_PORT: int = 12346
HEADER = 10  # lunghezza del header per inviare i messaggi
ENCODER = 'utf-8'  # codifica dei caratteri per inviare i messaggi
ipv4Protocol = socket.AF_INET
tcpProtocol = socket.SOCK_STREAM


class ClientX1:
    nickName = ""
    handShaking = False

    def __init__(self, nickname, host=HOST_IP, port=HOST_PORT):
        self.host = host
        self.port = port
        self.nickName = nickname
        self.server = socket.socket(ipv4Protocol, tcpProtocol)
        self.server.connect((self.host, self.port))


class clientObj:
    id = ""
    mail = ""
    _password = ""
    nickName = ""
    _hashId = ""

    def __init__(self, _nickName: str, _client: socket, _databaseName):
        self.conn = sqlite3.connect(_databaseName)
        self.cursor = self.conn.cursor()
        self.nickName = _nickName
        self.mail = ""
        self._password = ""
        self.clientSocket = _client
        self.ipAddress = self.clientSocket.getpeername()[0]
        """
                id INTEGER PRIMARY KEY,
                nickName TEXT NOT NULL,
                mail TEXT NOT NULL,
                password TEXT NOT NULL,
                hashId TEXT NOT NULL,
                isKicked INTEGER NOT NULL,
                isBlackListed INTEGER NOT NULL
        """
        result = self.getUserById(self.nickName, self.ipAddress)
        if result:
            self.id = result[0]
            self.mail = result[2]
            self._password = result[3]
            self._hashId = result[4]
            self.isKicked = result[5]
            self.isBlackListed = result[6]
        else:
            print("current user not in database and need to be registered")
            self.cursor.execute(
                """INSERT INTO users (nickName, mail, password, address, hashId, isKicked, isBlackListed)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (client.nickName, client.mail,
                 client._password, client._hashId,
                 client.isKicked, client.isBlackListed)
            )
            self.conn.commit()

    def getUserById(self, nickName, ipAddress):
        # Esegue una query per recuperare l'utente dal database
        self.cursor.execute("SELECT * FROM users WHERE id = %s AND ip_address = %s", (nickName, ipAddress))
        result = self.cursor.fetchone()
        self.cursor.close()
        return result

    def createHashId(self, _nickName):
        """
        l'hash table avrà questo aspetto:
                        CREATE TABLE IF NOT EXISTS user (
                        id INTEGER PRIMARY KEY,
                        nickName TEXT NOT NULL,
                        hashKey TEXT NOT NULL,
                        AESKey TEXT NOT NULL,
                        RSApublic TEXT NOT NULL,
                        RSAprivate TEXT NOT NULL
                    )
        :param _nickName:
        :return:
        """
        hashKey = cryptex.generateKeyHASH(self._password)
        aesKey = cryptex.generateKeyAES()
        rsaKeyPublic, rsaKeyPrivate = cryptex.generateKeysRSA()
        self.cursor.execute(
            """INSERT INTO users (nickName, hashKey, AESKey, RSApublic, RSAprivate)
               VALUES (?, ?, ?, ?, ?)""",
            (_nickName, hashKey,
             aesKey, rsaKeyPublic,
             rsaKeyPrivate)
        )
        self.conn.commit()

    def logIn(self, userName, _password):
        pass

    def sendMsg(self, header, message):
        self.clientSocket.send(header.encode(ENCODER))
        self.clientSocket.send(message.encode(ENCODER))


class DatabaseUtility:
    def __init__(self, _databaseName):
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
        pass

    def deleteATable(self, _table):
        pass

    def deleteAllTable(self):
        pass

    def __del__(self):
        # Chiudere la connessione a SQLite
        self.conn.close()


if __name__ == '__main__':
    db = DatabaseUtility("test01")
    aaaa = ClientX1("john")
    client = clientObj("john", aaaa, "test01")
    messageReceived = {"sender": "john", "timestamp": "11:11:00", "msgType": "text", "message": "HelloEveryBody"}
    db.storeMessage(messageReceived)
