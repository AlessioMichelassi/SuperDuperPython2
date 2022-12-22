import secrets
# pip install pycryptodomex
from Cryptodome.Cipher import AES

# Per generare le chiavi, puoi utilizzare il modulo:
from Cryptodome.PublicKey import RSA
# Per criptare e decriptare i messaggi, puoi utilizzare il modulo
from Cryptodome.Cipher import PKCS1_OAEP

import hashlib

"""
Esistono molti modi per criptare e decriptare i messaggi, a seconda delle tue esigenze di sicurezza e dei 
requisiti del tuo programma. Ecco alcune opzioni comuni: 

    Criptografia simmetrica: in questo caso, si utilizza la stessa chiave sia per criptare che per decriptare il 
    messaggio. Un esempio di criptografia simmetrica è l'algoritmo AES (Advanced Encryption Standard), 
    DES (Data Encryption Standard) e Blowfish. 

    Criptografia asimmetrica: in questo caso, si utilizzano due chiavi diverse per criptare e decriptare il 
    messaggio. Un esempio di criptografia asimmetrica è l'algoritmo RSA(Rivest-Shamir-Adleman) e 
    Elliptic Curve Cryptography (ECC). 

    Hash: un hash è una stringa di output di lunghezza fissa ottenuta da un input di qualsiasi lunghezza. Gli hash 
    vengono spesso utilizzati per verificare l'integrità dei dati o per criptare le password. Un esempio di algoritmo 
    di hash è SHA-256.
    
    Crittografia ibrida: in questo metodo, viene utilizzata una combinazione di crittografia a chiave simmetrica e 
    asimmetrica. Ad esempio, il messaggio potrebbe essere criptato con una chiave simmetrica e poi con una chiave 
    asimmetrica. 

    Crittografia a chiave a uso singolo (One-Time Pad): in questo metodo, viene utilizzata una chiave casuale per 
    criptare il messaggio. La chiave viene poi distrutta dopo l'utilizzo e non può essere utilizzata per
    decriptare altri messaggi. 

questa è una cosa che l'ai aggiunge rispetto al fatto che il giorno prima stavamo realizzando un programma di chat
server client:

            Per implementare la criptografia in un programma di chat, dovrai scegliere 
            un algoritmo di criptografia adeguato alle tue esigenze di sicurezza e utilizzarlo 
            per criptare e decriptare i messaggi degli utenti. Dovrai anche gestire la 
            distribuzione e il mantenimento delle chiavi di criptografia in modo sicuro. 

    Ecco alcune situazioni in cui potrebbe essere più adeguato utilizzare un determinato metodo di crittografia:

    Crittografia a chiave simmetrica: è solitamente più veloce dei metodi a chiave asimmetrica ed è 
    adeguato per la crittografia di grandi quantità di dati, come ad esempio il contenuto di un intero disco rigido o 
    di una rete di trasmissione. Tuttavia, richiede che entrambe le parti coinvolte condividano la chiave di 
    crittografia in modo sicuro, il che può essere difficile in alcune situazioni. 

    Crittografia a chiave asimmetrica: è solitamente più lento dei metodi a chiave simmetrica, 
    ma offre un maggiore livello di sicurezza poiché non è necessario condividere la chiave di crittografia. È 
    adeguato per la crittografia di piccole quantità di dati, come ad esempio messaggi di posta elettronica o file di 
    piccole dimensioni. 

    Crittografia ibrida: questo metodo combina le caratteristiche dei metodi a chiave simmetrica e asimmetrica, 
    offrendo velocità e sicurezza. È adeguato per la crittografia di quantità di dati di dimensioni moderate, 
    come ad esempio il contenuto di un database o di un file di grandi dimensioni. 

    Crittografia a chiave a uso singolo (One-Time Pad): questo metodo è il più sicuro in assoluto poiché utilizza una 
    chiave casuale per criptare il messaggio, che viene poi distrutta dopo l'utilizzo. Tuttavia, richiede che 
    entrambe le parti coinvolte condividano la chiave di crittografia in modo sicuro prima dell'invio del messaggio e 
    che la chiave sia sufficientemente lunga per garantire la sicurezza del messaggio. È adeguato per la crittografia 
    di messaggi di importanza critica o di alto livello di sicurezza.
    
    Il metodo di hash viene solitamente utilizzato per generare valori di hash univoci a partire da dati di input di 
    qualsiasi dimensione. I valori di hash vengono spesso utilizzati per effettuare il controllo dell'integrità dei 
    dati, poiché qualsiasi modifica apportata ai dati di input dovrebbe produrre un valore di hash completamente 
    diverso.
    
    Ecco alcune situazioni in cui potrebbe essere più adeguato utilizzare il metodo di hash:

    Verifica dell'integrità dei dati: il metodo di hash viene spesso utilizzato per verificare l'integrità dei dati 
    durante il trasferimento o lo storage. Ad esempio, se si scarica un file da Internet, è possibile utilizzare una 
    funzione di hash per calcolare il valore di hash del file scaricato e confrontarlo con il valore di hash fornito 
    dal fornitore del file. Se i due valori corrispondono, il file è probabilmente intatto e non è stato modificato 
    durante il trasferimento. 

    Archiviazione di password: il metodo di hash viene spesso utilizzato per archiviare le password in modo sicuro. 
    Invece di memorizzare le password in chiaro nel database, le password vengono elaborate attraverso una funzione 
    di hash e il valore di hash viene memorizzato al loro posto. In questo modo, anche se il database viene 
    compromesso, gli attaccanti non potranno ottenere le password originali. 

    Generazione di identificatori univoci: il metodo di hash viene spesso utilizzato per generare identificatori 
    univoci a partire da dati di input di qualsiasi dimensione. Ad esempio, il metodo di hash potrebbe essere 
    utilizzato per generare un identificatore univoco per un documento o per un record in un database. 

    Generazione di fingerprint digitali: il metodo di hash viene spesso utilizzato per generare "fingerprint 
    digitali" a partire da file, immagini o altri tipi di dati. Una fingerprint digitale è un valore di hash univoco 
    che rappresenta l'input originale e può essere utilizzata per individuare i duplicati o per verificare 
    l'integrità dei dati. 
 

Come puoi vedere, la scelta del metodo di crittografia più adeguato dipende dalle specifiche esigenze di sicurezza e 
dall'ambiente di utilizzo. In generale, però, è importante scegliere un metodo di crittografia robusto e affidabile 
per proteggere i dati sensibili. 

"""


class cryptex:

    @staticmethod
    def generateKeyAES():
        """
        Per generare una chiave, puoi utilizzare il modulo secrets di Python,
        che fornisce funzionalità per generare chiavi sicure casuali
        :return:
        """
        key = secrets.token_bytes(16)  # Genera una chiave di 16 byte
        return key

    # ####################################################################################
    #
    #   Queste funzioni utilizzano il modo di
    #   cifratura EAX (Authenticated Encryption with Associated Data),
    #   che fornisce autenticazione e integrità dei dati oltre alla privacy.
    #

    @staticmethod
    def encryptAES(_key, _message):
        """
        Cripta un messaggio utilizzando il metodo Aes.

        Il tag e il nonce (numero usato una volta, in inglese "nonce") sono entrambi
        informazioni aggiuntive utilizzate durante la cifratura e la decifratura
        dei messaggi utilizzando il modo di cifratura EAX (Authenticated Encryption with Associated Data)
        di AES (Advanced Encryption Standard).

        Il tag è una stringa di byte che viene calcolata durante la cifratura
        del messaggio e utilizzata durante la decifratura per verificare
        l'integrità del messaggio.

        Se il messaggio è stato modificato in qualsiasi modo durante il trasferimento,
        il tag non corrisponderà al messaggio decifrato e la decifratura fallirà.

        Il nonce è un numero casuale utilizzato durante la cifratura per evitare
        che i messaggi cifrati possano essere facilmente attaccati utilizzando
        tecniche di "replay attack".

        Ogni volta che viene cifrato un nuovo messaggio,
        deve essere utilizzato un nuovo nonce.

        Durante la cifratura, il tag e il nonce vengono calcolati e
        restituiti insieme al messaggio cifrato.

        Durante la decifratura, il tag e il nonce devono essere forniti
        nuovamente insieme al messaggio cifrato per consentire
        la verifica dell'integrità del messaggio e
        l'utilizzo del nonce corretto per decifrare il messaggio.

        :param _key: la chiave per il criptaggio del messaggio
        :param _message: il messaggio in formato testo o in formato bytes
                        se il testo è una stringa, viene convertito automaticamente in bytes
        :return: il testo cifrato, il tag e il nounce
        """
        if type(_message) is not bytes:
            messageBytes = bytes(_message, "utf-8")
        else:
            messageBytes = _message
        cipher = AES.new(_key, AES.MODE_EAX)
        _ciphertext, _tag = cipher.encrypt_and_digest(messageBytes)
        return _ciphertext, _tag, cipher.nonce

    @staticmethod
    def decryptAES(_key, _ciphertext, _tag, _nonce):
        cipher = AES.new(_key, AES.MODE_EAX, _nonce)
        _message = cipher.decrypt_and_verify(_ciphertext, _tag)
        return _message

    # ####################################################################################
    #
    #   per generare coppie di chiavi pubbliche e private e utilizzarle per criptare
    #   e decriptare i messaggi utilizzando l'algoritmo di criptografia asimmetrica
    #   RSA (Rivest-Shamir-Adleman).
    #

    @staticmethod
    def generateKeysRSA():
        """
        In una coppia di chiavi pubblica/privata RSA, la chiave pubblica viene utilizzata
        per criptare i dati e verificare la firma digitale, mentre la chiave privata
        viene utilizzata per decifrare i dati e firmare digitalmente i documenti.
        Di solito, la chiave pubblica viene condivisa con gli altri, mentre la chiave privata
        viene tenuta segreta e protetta dal proprietario.

        In caso di distruzione o smarrimento della chiave pubblica, non sarà più possibile
        decriptare i dati o recuperare la chiave pubblica a partire dalla chiave privata.
        La chiave pubblica e la chiave privata sono generate insieme e sono
        strettamente legate, ma non sono reciprocamente derivabili.

        Se si perde la chiave pubblica, non c'è modo di recuperarla. Tuttavia, è possibile
        generare una nuova coppia di chiavi pubblica/privata e distribuire la
        nuova chiave pubblica agli utenti che ne hanno bisogno.

        È importante conservare la chiave privata in modo sicuro, poiché è necessaria
        per decifrare i dati criptati con la chiave pubblica e per firmare digitalmente i
        documenti.

        In teoria, il server potrebbe conservare sia la chiave pubblica che la chiave privata
        del client, in modo da poter fornire la chiave pubblica al client in caso di perdita.

        Tuttavia, ciò implicherebbe che il server possiede anche la chiave privata del client,
        il che potrebbe comportare dei rischi per la sicurezza dei dati.

        Se il server viene compromesso o viene a conoscenza di terzi della chiave privata del client,
        potrebbero verificarsi problemi di sicurezza.

        Pertanto, è generalmente consigliabile che il client conservi personalmente sia la
        chiave pubblica che la chiave privata e che le protegga adeguatamente.

        Se la chiave pubblica viene persa, il client può sempre generare una nuova coppia
        di chiavi pubblica/privata e distribuire la nuova chiave pubblica
        agli utenti che ne hanno bisogno.

        :return: una tupla contenente la chiave pubblica e quella privata
        """
        key = RSA.generate(2048)  # Genera una coppia di chiavi con una lunghezza di 2048 bit
        privateKey = key.export_key()
        publicKey = key.publickey().export_key()
        return privateKey, publicKey

    @staticmethod
    def encryptRSA(_publicKey, _message):
        if type(_message) is not bytes:
            messageBytes = bytes(_message, "utf-8")
        else:
            messageBytes = _message
        pk = _publicKey.decode("UTF-8")
        if pk.startswith("-----BEGIN PUBLIC KEY-----"):
            print("correct public key")
            _publicKeyZ = RSA.import_key(_publicKey)
            cipher = PKCS1_OAEP.new(_publicKeyZ)
            _ciphertext = cipher.encrypt(messageBytes)
            return _ciphertext
        else:
            print("you need to provide a public key")
            return None

    @staticmethod
    def decryptRSA(_privateKey, _ciphertext: bytes):
        """
        Decripta un codice bytes se viene fornita una chiave RSA privata
        :param _privateKey: la chiave RSA in formato bytes
        :param _ciphertext: il testo criptato in formato bytes
        :return: il codice decriptato
        """
        pk = _privateKey.decode("UTF-8")
        if pk.startswith("-----BEGIN RSA PRIVATE KEY-----"):
            print("correct public key")
            _privateKeyZ = RSA.import_key(_privateKey)
            cipher = PKCS1_OAEP.new(_privateKeyZ)
            returnMessage = cipher.decrypt(_ciphertext)
            return returnMessage
        else:
            print("you need to provide a private key")
            return None

    # ####################################################################################
    #
    #   Ecco un esempio di come potrebbe funzionare l'utilizzo di una funzione
    #   di hash per crittografare una password:
    #
    #     L'utente sceglie una password, ad esempio "password123".
    #     La password viene inserita in una funzione di hash, come ad esempio SHA-256.
    #     La funzione di hash elabora la password e produce un valore di hash univoco,
    #     come ad esempio "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92".
    #     Il valore di hash viene memorizzato al posto della password in chiaro nel database.
    #     Quando l'utente inserisce nuovamente la password per effettuare l'accesso,
    #     la password viene nuovamente elaborata dalla funzione di hash e viene confrontata
    #     con il valore di hash memorizzato nel database. Se i due valori corrispondono,
    #     l'accesso viene consentito, altrimenti viene negato.
    #
    #     È importante notare che le funzioni di hash sono progettate in modo tale
    #     da essere facilmente calcolabili in una direzione (ad esempio, trasformare
    #     la password in un valore di hash), ma molto difficili da invertire
    #     (ad esempio, calcolare la password originale a partire dal valore di hash).
    #     Ciò rende difficile per gli attaccanti ottenere le password originali
    #     anche se riescono a ottenere il database con i valori di hash.

    @staticmethod
    def generateKeyHASH(text: str) -> bytes:
        """
        Genera una chiave di crittografia
        :param text: il testo per generare una chiave come ad esempio una password
        :return:
        """
        return hashlib.sha256(text.encode('utf-8')).digest()

    @staticmethod
    def encrypt(_key: bytes, _message: str) -> bytes:
        """
        Ecoder HASH
        :param _key: una chiave generata con la funzione generate Hash
        :param _message: un messaggio di testo
        :return:
        """
        # Utilizzo di XOR per criptare il messaggio
        encryptedMessage = bytearray(len(_message))
        for i, c in enumerate(_message):
            encryptedMessage[i] = _key[i % len(_key)] ^ ord(c)
        return bytes(encryptedMessage)

    def decrypt(_key: bytes, _encryptedMessage: bytes) -> str:
        """
        Decriptazione del messaggio
        :param _encryptedMessage:
        :return:
        """
        # Utilizzo di XOR per decriptare il messaggio
        _decryptedMessage = bytearray(len(_encryptedMessage))
        for i, c in enumerate(_encryptedMessage):
            _decryptedMessage[i] = _key[i % len(_key)] ^ c
        return _decryptedMessage.decode('utf-8')


if __name__ == '__main__':
    print("TESTING FUNCTION AES")
    print("*" * 20)
    crypt = cryptex()
    keyAes = crypt.generateKeyAES()
    print(keyAes)
    message = "the quick brown fox jump over the lazy dog."
    print(f"originalMessage: {message}")

    ciphertext, tag, nonce = crypt.encryptAES(keyAes, message)

    print(f"the text is encrypted.\nCrypt = {ciphertext}\nTag = {tag}\nNonce = {nonce}")
    deCipherMessage = crypt.decryptAES(keyAes, ciphertext, tag, nonce)
    print(f"decrypted Message:\n{deCipherMessage}")
    print("\n\n")
    print("TESTING FUNCTION RSA")
    print("*" * 20)
    privateRsaKey, publicKeyRsa = crypt.generateKeysRSA()
    print(f"private RSA KEY = {privateRsaKey}")
    print(f"public RSA KEY = {publicKeyRsa}")
    print(f"message: {message}")
    encryptedText = crypt.encryptRSA(publicKeyRsa, message)
    print(encryptedText)
    decryptedText = crypt.decryptRSA(privateRsaKey, encryptedText)
    print(decryptedText)
