# Per generare le chiavi, puoi utilizzare il modulo:
from Cryptodome.PublicKey import RSA
# Per criptare e decriptare i messaggi, puoi utilizzare il modulo
from Cryptodome.Cipher import PKCS1_OAEP


def generateKeysRSA():
    key = RSA.generate(2048)  # Genera una coppia di chiavi con una lunghezza di 2048 bit
    privateKey = key.export_key()
    publicKey = key.publickey().export_key()
    return privateKey, publicKey


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


message = "the quick brown fox jump over the lazy dog"
print("TESTING FUNCTION RSA")
print("*" * 20)
privateRsaKey, publicKeyRsa = generateKeysRSA()
print(f"private RSA KEY = {privateRsaKey}")
print(f"public RSA KEY = {publicKeyRsa}")
print(f"message: {message}")
encryptedText = encryptRSA(publicKeyRsa, message)
print(encryptedText)

decryptedText = decryptRSA(privateRsaKey, encryptedText)
print(decryptedText)
