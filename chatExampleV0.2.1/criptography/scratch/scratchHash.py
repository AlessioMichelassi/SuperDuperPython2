import hashlib


# Generazione della chiave di crittografia
def generateKeyHASH(password: str) -> bytes:
    return hashlib.sha256(password.encode('utf-8')).digest()


# Criptazione del messaggio
def encrypt(_key: bytes, _message: str) -> bytes:
    # Utilizzo di XOR per criptare il messaggio
    encryptedMessage = bytearray(len(_message))
    for i, c in enumerate(_message):
        encryptedMessage[i] = _key[i % len(_key)] ^ ord(c)
    return bytes(encryptedMessage)


# Decriptazione del messaggio
def decrypt(_key: bytes, _encryptedMessage: bytes) -> str:
    # Utilizzo di XOR per decriptare il messaggio
    _decryptedMessage = bytearray(len(_encryptedMessage))
    for i, c in enumerate(_encryptedMessage):
        _decryptedMessage[i] = _key[i % len(_key)] ^ c
    return _decryptedMessage.decode('utf-8')


# Generazione della chiave di crittografia
key = generateKeyHASH('password123')

# Criptazione del messaggio
message = "Ciao, come va?"
encrypted_message = encrypt(key, message)

# Decriptazione del messaggio
decrypted_message = decrypt(key, encrypted_message)

print(f'Messaggio originale: {message}')
print(f'Messaggio criptato: {encrypted_message}')
print(f'Messaggio decriptato: {decrypted_message}')
