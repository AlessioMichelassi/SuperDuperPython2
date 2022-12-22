import socket
import threading
import json
from datetime import datetime
from typing import Any

# ------------------------------------
#               CONSTANT

ipv4Protocol = socket.AF_INET
tcpProtocol = socket.SOCK_STREAM

# Define socket constants to be used and ALTERED
hostName = socket.gethostname()
HOST_IP = socket.gethostbyname(hostName)
HOST_PORT: int = 12346
HEADER = 10
ENCODER = 'utf-8'
# timeout in seconds
TIMEOUT = 10


# To do modificare la classe in modo che l'handShaking sia gestito
# da questo oggetto tramite log in
# modifica di alcuni comandi utente:
#                                   cambiare /exit con /disconnect o /quit
#                                   aggiungere /ignore <nickname utente>
#                                   aggiungere /me <text> scrive il messaggio in terza persona a caratteri maiuscoli
#                                   aggiungere /query <nickname> per creare un chat privata con uno o più utenti
#                                   aggiungere /invite <nick> <#channel/#chatprivata> per aggiungere utenti alla
#                                                                                        chat privata

# implementare il log in da superUser
# come super user deve essere possibile utilizzare i comandi shell per gestire il server
# possibilità di cambiare la password e criptarla
# aggiunta di un database per gli utenti e i file caricati sul server
# implementare la possibilità di mandare file di grandi dimensioni
# implementare la possibilità di fare uno streaming


class clientObj:

    def __init__(self, name: str, client: socket, address):
        self.nickName = name
        self.mail = ""
        self.password = ""
        self.clientSocket = client
        self.ipAddress = address

    def logIn(self, userName, _password):
        pass
    
    def sendMsg(self, header, message):
        self.clientSocket.send(header.encode(ENCODER))
        self.clientSocket.send(message.encode(ENCODER))


class ClientThread(threading.Thread):

    def __init__(self, _client: clientObj, _server: 'ServerX'):
        threading.Thread.__init__(self)
        self.client: clientObj = _client
        self.server = _server
        self.isRunning = True

    def run(self):

        while True:
            # ricevi il messaggio dal client
            try:
                self.server.handleMessageReception(self.client)
                if not self.isRunning:
                    print(f"message from thread {self.client.nickName}: thread closed!")
                    break
            except Exception as e:
                print(f"exception in thread {self.client.nickName} - the thread will be stopped")
                self.isRunning = False
                self.stop()
                break

    def stop(self):
        try:
            self.isRunning = False
            self.join()
            self.client.clientSocket.close()
            print(f"message from thread {self.client.nickName}:\nthread stopped\nself.isRunning = {self.isRunning}")
        except Exception as e:
            print(f"exception in stop function of thread {self.client.nickName}: {e}")


class ServerX:
    clients: dict = {}
    blacklist = []
    kickedClient = []
    lastMessage = ""
    isServerOn = True
    threadList = {}

    def __init__(self, host=HOST_IP, port=HOST_PORT):
        self.host = host
        self.port = port
        self.server = socket.socket(ipv4Protocol, tcpProtocol)
        # imposta il socket per riutilizzare l'indirizzo
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.blacklist = []
        self.kickedClient = []
        self.clients: dict = {}
        try:
            """
            il server prova a connettersi all'indirizzo specificato,
            nel caso di problemi chiude l'eventuale connessione precedente
            ed esce dal programma
            """
            self.server.bind((self.host, self.port))
            self.server.listen()
            print(f"server connected: {self.host}:{self.port}")
            print("waiting for incoming connection...\n")
            while True:
                try:
                    client, address = self.server.accept()
                    if client not in self.kickedClient or client not in self.blacklist:
                        self.sendWelcomeHandShake(client, address)
                except socket.timeout:
                    print("client gone")
                except ConnectionResetError as e:
                    # il client ha chiuso la connessione
                    print(f"client gone {e}")

        except OSError:
            print("Failed to start server: address already in use\n")
            # chiudi il socket del server
            self.server.close()
            # gestisci l'errore come desideri, ad esempio chiedendo all'utente di scegliere un altro indirizzo o porta
            # oppure chiudendo il programma
            exit()

    @staticmethod
    def stampMessage(messageType, message):
        """
        Crea un prototipo di messaggio. Ogni messaggio inviato,
        è un file jSon che deve contenere:
                       "sender": "Server",
                       "date": f"{currentTime}",
                       "msgType": f"{messageType}",
                       "message": f"{message}"}
        :param messageType: i tipi di messaggio del server possono essere:
                            error, text, handShake,
         :param message: il messaggio di testo da allegare
         :return: un file jSon
        """
        currentDateAndTime = datetime.now()
        currentTime = currentDateAndTime.strftime("%H:%M:%S")
        unjSonedMsg = {"sender": "Server",
                       "date": f"{currentTime}",
                       "msgType": f"{messageType}",
                       "message": f"{message}"}
        return json.dumps(unjSonedMsg)

    @staticmethod
    def sendMessage(message: json, client: clientObj):
        """
        Manda un messaggio a un singolo client
        :param message: il messaggio jSon
        :param client: il client in formato clientObj
        :return:
        """
        header = str(len(message))
        while len(header) < HEADER:
            header += " "
        client.sendMsg(header, message)

    def sendMsgToAll(self, message: json, clientToExclude=None):
        """
        Manda un messaggio a tutti i client della lista,
        il messaggio può essere un nuovo messaggio dal Server verso tutti
        oppure un messaggio mandato da un client e ribattuto verso tutti gli altri
        :param message:
        :param clientToExclude:
        :return:
        """
        if type(message) is dict:
            unjSonedMsg = {"sender": f"{message['sender']}",
                           "date": f"{message['date']}",
                           "msgType": f"{message['msgType']}",
                           "message": f"{message['message']}"}
            msg = json.dumps(unjSonedMsg)
        else:
            msg = message
        try:
            header = str(len(msg))
            while len(header) < HEADER:
                header += " "
            for client in self.clients.values():
                if client.nickName != clientToExclude.nickName:
                    client.sendMsg(header, msg)
        except Exception as e:
            print(f"debug error: #{msg}     #")
            print(e)

    def sendWelcomeHandShake(self, client: socket, address):
        """
        Controlla che il client non sia nella lista dei cattivi
        altrimenti lo registra.
        Manda un messaggio di handShake
        dove chiede al client il nickName.
        Si differenzia da sendMessage perchè per mandarlo utilizza
        l'indirizzo socket del client non ancora registrato
        :param address: ip address
        :param message: messaggio jSon
        :param client: client in formato socket
        """
        print(f"incoming connection from [{address}]\n")
        if address in self.blacklist:
            refuseConnectionMessage = self.stampMessage("error", "sorry you cannot enter in this chat")
            self.sendHandShakeMessage(refuseConnectionMessage, client)
            client.close()
            print("client kicked")
        else:
            self.handShake(client, address)

    def handShake(self, client, address):
        """
        Questa funzione registra i client se il nickname
        non è già presente nella lista dei nickName.
        In caso affermativo il server manda un messaggio di ACK
        :param client: socket
        :param address: ip
        :return:
        """
        handShakeMsg = self.stampMessage("handShake", "NICK")
        self.sendHandShakeMessage(handShakeMsg, client)
        handShakeReturn = self.receiveMessage(client)
        nickName = handShakeReturn["message"]
        if nickName not in self.clients and nickName not in self.clients.values():
            handShakeMsg = self.stampMessage("handShake", "ACK")
            self.sendHandShakeMessage(handShakeMsg, client)
            self.connectClient(client, address, nickName)
        else:
            handShakeMsg = self.stampMessage("handShake", "KICK")
            self.sendHandShakeMessage(handShakeMsg, client)
            print("connection refused with: {nickName}")
            client.close()

    @staticmethod
    def sendHandShakeMessage(message, client):
        header = str(len(message))
        while len(header) < HEADER:
            header += " "
        client.send(header.encode(ENCODER))
        client.send(message.encode(ENCODER))

    def receiveMessage(self, client: socket):
        """
        Quando il client si connette la prima volta, il server
        usa questa funzione per ricevere i messaggi. Li usa solo
        per fare l'handShake.
        :param client: client in formato socket
        :return:
        """
        if client in self.kickedClient and client in self.blacklist:
            msg = self.stampMessage("WARNING", "because you are banned from the jungle you cannot send any msg")
            self.sendMessage(msg, client)
        else:
            bufferSize = client.recv(HEADER).decode(ENCODER)
            jsonMsgReceived = client.recv(int(bufferSize)).decode(ENCODER)
            print(f"messageReceived: {jsonMsgReceived}")
            return json.loads(jsonMsgReceived)

    def handleMessageReception(self, client: clientObj):
        """
        Una volta che il client è registrato con un nickName,
        i suoi messaggi vengono registrati con questa funzione
        :param client: client di tipo clientObj
        :return:
        """
        if client in self.kickedClient and client in self.blacklist:
            msg = self.stampMessage("WARNING", f"{client.nickName}because you are banned from the jungle you cannot "
                                               f"send any msg")
            self.sendMessage(msg, client)
        else:
            bufferSize = client.clientSocket.recv(HEADER).decode(ENCODER)
            if not len(bufferSize):
                print("client disconnected")
                self.removeClientByNickname(self.clients, client.nickName)
                return
            jsonMsgReceived = client.clientSocket.recv(int(bufferSize)).decode(ENCODER)
            print(f"messageReceived: {jsonMsgReceived}")
            message = json.loads(jsonMsgReceived)
            self.handleClient(message, client)

    def connectClient(self, _client, _address, _nickName: str):
        """
        Se il client è stato accettato viene connesso alla chat,
        il server gli manda il benvenuto e fa partire i thread
        per i messaggi in ingresso.
        :param _client:
        :param _address:
        :param _nickName:
        :return:
        """
        client = clientObj(_nickName, _client, _address)
        self.clients[client.nickName] = client
        welcomeMsg = self.stampMessage("text", f"Welcome to the Jungle {client.nickName}")
        self.sendMessage(welcomeMsg, client)
        msg = self.stampMessage("text", f"{client.nickName} joined us in the jungle.")

        self.sendMsgToAll(msg, client)
        receiveThread = ClientThread(client, self)
        self.threadList[_nickName] = receiveThread
        receiveThread.start()

    # ##################################################################
    #
    #                        main thread for listen
    #
    #

    def handleClient(self, message: dict, client: clientObj):
        """
        Ogni client può mandare dei comandi al server.
        La lista dei comandi è accessibile tramite /help.
        Il comando /exit creava dei problemi ed è stato utilizzato
        un metodo alternativo
        :param message:
        :param client:
        :return:
        """
        if message["msgType"] == "text":
            self.sendMsgToAll(message, client)
        elif message["msgType"] == "exit":
            self.exitClient(client)
        elif message["msgType"] == "root":
            self.logIn(client)
        elif message["msgType"] == "rootPassword":
            print("rootPassword")
            if message["message"] == "/rootPass 123456":
                self.connectClientAsRoot(client)
        elif message["msgType"] == "command":
            self.handleCommonCommand(message, client)
            return False
        else:
            return True

    def handleCommonCommand(self, message: dict, client: clientObj):
        command = message["message"][1:]
        if command != "":
            sender = message["sender"]
            if command.startswith("help"):
                print("helpCommand")
                self.sendHelp(client)
            elif command.startswith("nick"):
                newNickname = command.replace("nick", "").rsplit()
                if newNickname != "root":
                    self.changeNickName(newNickname, client)
                else:
                    self.sendMessage(self.stampMessage("error", "You cannot use root name"), client)
            elif command.startswith("kick"):
                self.kickClient(command, client)
            elif command == "join":
                # implementa la funzionalità di join qui
                pass
            elif command == "leave":
                # implementa la funzionalità di leave qui
                pass
            elif command == "list":
                self.showUserList(client)
            elif command == "who" and sender == "root":
                self.whoFunction(message["message"], client)
            elif command == "msgTo":
                print("msgTo")
                self.sendPrivateMessage(message, client)
            else:
                self.sendMessage(self.stampMessage("error", f"the command you wrote was wrong...\n{message}"),
                                 client)

    # ##################################################################
    #
    #                        Server Command Function
    #
    #

    def sendHelp(self, client):
        self.sendMessage(self.stampMessage("info", "\n\nList of available commands:\n\t"
                                                   "/nick <new_nickname>\n\t"
                                                   "/createChannel <channel_name> *to be implemented\n\t"
                                                   "/joinChannel <channel_name> *to be implemented\n\t"
                                                   "/leaveChannel *to be implemented\n\t"
                                                   "/list\n\t"
                                                   "/whoIs <nickname>\n\t"
                                                   "/kick <nickname>\n\t"
                                                   "/msg <nickname> <message>\n\t"
                                                   "/exit"), client)

    def changeNickName(self, newNickname: str, client: clientObj):
        if newNickname not in self.clients.values():
            print(f"{self.clients}")
            client.nickName = newNickname

            handShakeMsg = self.stampMessage("commandNick", f"ACK::{newNickname}")
            self.sendMessage(handShakeMsg, client)
            self.sendMessage(self.stampMessage("command", f"Your nickname has been changed to {client.nickName}"),
                             client)
        else:
            self.sendMessage(self.stampMessage("command", "Sorry nickname has taken.. choose anotherOne.."), client)

    def showUserList(self, clientToSend):
        """
        Mostra la lista di utenti presenti in chat
        :param clientToSend: il client a cui mandare indietro la lista
        """
        if clientToSend.nickName == "root":
            users = []
            clientsNickname = self.clients.keys()
            clientList = self.clients.values()
            msg = f"your majesty this is the list of the nicknames:\n {clientsNickname}"
            msgK = self.stampMessage("info", msg)
            self.sendMessage(msgK, clientToSend)
            for client in clientList:
                clientAddress = client.clientSocket.getpeername()
                client_ip, client_port = clientAddress[0], clientAddress[1]
                users.append(f"client : {client_ip}:{client_port} - nickName: {client.nickName}")

            retMessage = "this is the detailedList:\n"
            for string in users:
                retMessage += f"{string}\n"

            msg = self.stampMessage("info", retMessage)
            self.sendMessage(msg, clientToSend)
        else:
            print(f"non root find in {clientToSend.nickName}")

    def whoFunction(self, message, sender: clientObj):
        """
        dato in nome del client ritorna i suoi dati.
        :param sender: generally the root user
        :param message:
        :return:
        """
        name = message.split()
        clientToSearch = ""
        if sender.nickName == "root":
            for client in self.clients.values():
                if client.nickName == name:
                    clientToSearch = client
                else:
                    msg = self.stampMessage("error", f"the client with name: {message} was not found...")
                    self.sendMessage(msg, sender)
                    return
            if clientToSearch != "":
                clientAddress = clientToSearch.clientSocket.getpeername()
                client_ip, client_port = clientAddress[0], clientAddress[1]
                response = self.stampMessage("info", f"result for {name}:\n\t"
                                                     f"ip: {client_ip} port: {client_port}\n\t"
                                                     f"nickname: {clientToSearch.nickname}")
                self.sendMessage(response, sender)

    def getClientByNickname(self, nickname: str) -> Any | None:
        # sourcery skip: use-next
        """
        Cerca un client nella lista dei client connessi tramite il nickname
        :param nickname: il nickname del client da cercare
        :return: il client connesso con il nickname specificato, se esiste
        """
        for client in self.clients.values():
            if client.nickName == nickname:
                return client
        return None

    def stopClientThreadByNickname(self, nickname: str):
        # sourcery skip: use-next
        """
        Cerca un thread nel dizionario dei thread connessi tramite il nickname
        :param nickname: il nickname del client da cercare
        :return: frma in thread
        """
        if nickname in self.clients:
            thread = self.threadList[nickname]
            thread.isRunning = False
            thread.stop()
            thread.join()
            del self.threadList[nickname]
        else:
            print("Thread not found")

    def removeClientByNickname(self, clients: dict, nickname: str, isBanned=False):
        # codifica il nickname in UTF-8
        # cerca il client con il nickname specificato
        for clientNickname, clientObject in clients.items():
            if clientNickname == nickname:
                if isBanned:
                    kickMsg = self.stampMessage("EXIT", "you are kicked out from this chat")
                    self.sendMessage(kickMsg, clientObject)
                    self.kickedClient.append(clientObject)
                    self.stopClientThreadByNickname(nickname)
                # rimuovi il client dal dizionario
                clients.pop(clientNickname, None)
                # chiudi la connessione con il client
                clientObject.clientSocket.close()
                return "ACK"
        # il client non è stato trovato
        return f"Client with nickname '{nickname}' not found"

    def kickClient(self, command, client: clientObj):
        """
        espelle un client
        :param command: nel command c'è il nome del client
        :param client:
        :return:
        """
        nicknameToKick = command.replace("kick", "").rsplit()
        if type(nicknameToKick) == list:
            nicknameToKick = nicknameToKick[0]
            print(f"kick funzione3: {nicknameToKick}")
        if type(nicknameToKick) == bytes:
            nicknameToKick = str(nicknameToKick, 'utf-8')
            print(f"kick funzione4: {nicknameToKick}")
        if nicknameToKick == client.nickName:
            msgToClient = self.stampMessage("error", f"{client.nickName} you cannot kick yourself!")
            self.sendMessage(msgToClient, client)
            return
        if client.nickName == "root" and nicknameToKick != "root":
            response = self.removeClientByNickname(self.clients, nicknameToKick)
            if response == "ACK":
                msgToRoot = self.stampMessage("root", f"{nicknameToKick} was kicked out from this this chat")
            else:
                msgToRoot = self.stampMessage("root", f"{response} ")
            self.sendMessage(msgToRoot, client)
        else:
            self.sendMessage(self.stampMessage("error", "Only root can kick clients"), client)

    def sendPrivateMessage(self, message: json, sender: clientObj):
        """
        Manda un messaggio privato un certo utente.
        :param message:
        :param sender:
        :return:
        """
        # sourcery skip: use-next
        # estrai il nickname del destinatario
        # e il contenuto del messaggio dal messaggio json
        try:
            recipient = message["recipient"]
            msg = message["message"]
        except Exception as e:
            # send a message to client
            a = e
            return

        # verifica che il destinatario esista
        if recipient not in self.clients.values():
            # invia un messaggio di errore al mittente se il destinatario non esiste
            errorMessage = self.stampMessage("error", f"Nickname '{recipient}' not found")
            self.sendMessage(errorMessage, sender)
            return

        # cerca il socket del destinatario
        recipientSocket = self.clients[recipient]

        # verifica che il mittente sia autorizzato a inviare messaggi privati al destinatario
        if sender not in self.clients.values():
            # invia un messaggio di errore al mittente se non è autorizzato a inviare messaggi privati
            errorMessage = self.stampMessage("error", "You are not authorized to send private messages")
            self.sendMessage(errorMessage, sender)
            return

        # invia il messaggio privato al destinatario
        privateMessage = self.stampMessage("private", msg)
        try:
            self.sendMessage(privateMessage, recipientSocket)
        except Exception as e:
            # invia un messaggio di errore al mittente se il messaggio non può essere inviato al destinatario
            errorMessage = self.stampMessage("error", f"Unable to send message to '{recipient}': {e}")
            self.sendMessage(errorMessage, sender)

    def exitClient(self, client: clientObj):
        """
        when a client send /exit command
        :param client:
        :return:
        """
        name = client.nickName
        print(f"{name} has left the jungle...")
        self.stopClientThreadByNickname(name)
        response = self.removeClientByNickname(self.clients, name)
        if response == "ACK":
            self.sendMsgToAll(f"{name} has left the jungle...", client)
        else:
            msgToRoot = self.stampMessage("text", f"{response} ")
            print(f"error: {msgToRoot}")
        del self.clients[name]

    def logIn(self, client):
        self.sendMessage(self.stampMessage("root", "please insert the password"), client)

    def connectClientAsRoot(self, client):
        self.changeNickName("root", client)
        handShakeMsg = self.stampMessage("commandNick", f"ACK::{client.nickName}")
        self.sendMessage(handShakeMsg, client)
        self.sendMessage(self.stampMessage("command", "Your majesty, welcome back to the jungle"), client)


if __name__ == '__main__':
    server = ServerX()
