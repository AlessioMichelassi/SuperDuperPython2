import json
import threading
import socket
import time
from datetime import datetime

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
        self.handShakingLoop()

    def stampMessage(self, messageType, message):
        """
        Crea un prototipo di messaggio. Ogni messaggio inviato,
        è un file jSon che deve contenere:
                       "sender": "nickname",
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
        unjSonedMsg = {"sender": self.nickName,
                       "date": f"{currentTime}",
                       "msgType": f"{messageType}",
                       "message": f"{message}"}
        return json.dumps(unjSonedMsg)

    def sendMessage(self, message: json):
        """
        MAnda un messaggio a un singolo client
        :param message: il messaggio jSon
        :return:
        """
        header = str(len(message))
        while len(header) < HEADER:
            header += " "
        self.server.send(header.encode(ENCODER))
        # a questo punto codifica il messaggio in json che ritorna una stringa in bytes
        self.server.send(message.encode(ENCODER))

    def receiveMessage(self):
        bufferSize = self.server.recv(HEADER).decode(ENCODER)
        jsonMsgReceived = self.server.recv(int(bufferSize)).decode(ENCODER)
        print(f"messageReceived: {jsonMsgReceived}")
        return json.loads(jsonMsgReceived)

    @staticmethod
    def askNickname():
        return input("Inserisci il tuo nickname: ")

    def handShakingLoop(self):
        while not self.handShaking:
            msgRcv = self.receiveMessage()
            sender = msgRcv["sender"]
            msgType = msgRcv["msgType"]
            if sender == "Server" and msgType == "handShake":
                if msgRcv["message"] == "ACK":
                    print("HandShaking with server Ok!")
                    self.handShaking = True
                elif msgRcv["message"] == "KICK":
                    print("server kicked out from the chat\n please try using different nickname\n")
                    nick = self.nickName
                    while nick == self.nickName:
                        nick = self.askNickname()
                    self.nickName = nick
                    self.server.close()
                    self.server = socket.socket(ipv4Protocol, tcpProtocol)
                    self.server.connect((self.host, self.port))
                    # msg = self.stampMessage("handShake", self.nickName)
                    # self.sendMessage(msg)
                elif msgRcv["message"] == "NICK":
                    msg = self.stampMessage("handShake", self.nickName)
                    self.sendMessage(msg)

        # Avvia il client in un thread separato per l'invio dei messaggi
        send_Thread = threading.Thread(target=self.sendMessageThread)
        send_Thread.start()
        receive_Thread = threading.Thread(target=self.handleIncomingMessage)
        receive_Thread.start()

    def handleIncomingMessage(self):
        while True:
            try:
                msgRcv = self.receiveMessage()
                sender = msgRcv["sender"]
                msgType = msgRcv["msgType"]
                date = msgRcv["date"]
                message = msgRcv["message"]
                if sender == "Server":
                    print("WARNING - Message from Server")
                if msgType == "error":
                    print("WARNING there is an error")
                elif msgType == "private":
                    print("Someone send you a private message")
                elif msgType == "commandNick" and sender == "Server":
                    if "ACK::" in message:
                        self.nickName = message.replace("ACK::", "")
                elif msgType == "root" and sender == "Server":
                    print("SERVER SAID")
                print(f"{date} message received from {sender}:\n\t{message}")
            except Exception as e:
                print("*** Exception")
                print(f"\t{e}")
                self.server.close()
                break

    def sendMessageThread(self):
        print("receive thread")
        while True:
            message = input(f"{self.nickName}: ")
            if message.startswith("/"):
                command = message.replace("/", "")
                if command == "exit":
                    msg = self.stampMessage("exit", "i leave")
                    self.sendMessage(msg)
                    time.sleep(0.5)
                    self.server.close()
                    exit()
                elif command == "kick":
                    checkMessage = command.split()
                    try:
                        if not checkMessage[1]:
                            print("you cannot kick your self!")
                    except Exception as e:
                        print("error! did you mean: Kick <nickname>?")
                elif command == "msgTo":
                    recipient = input("insert the recipient: ")
                    message = input(f"msg to {recipient}: ")
                    msgTo = self.stampMessage("msgTo", f"/msgTo {message}")
                    self.sendMessage(msgTo)
                    return
                elif command == "root":
                    rootMsg = self.stampMessage("root", "")
                    self.sendMessage(rootMsg)
                elif "rootPass" in command:
                    rootMsg = self.stampMessage("rootPassword", f"{message}")
                    self.sendMessage(rootMsg)
                else:
                    commandMsg = self.stampMessage("command", f"{message}")
                    self.sendMessage(commandMsg)
            else:
                msg = self.stampMessage("text", message)
                self.sendMessage(msg)


if __name__ == '__main__':
    client = ClientX1("test2")