"""
Ecco un esempio di come potrebbe essere possibile utilizzare Python e la libreria pycryptodome per criptare e
decriptare un messaggio utilizzando l'algoritmo di crittografia a chiave simmetrica DES (Data Encryption Standard):

Nell'esempio sopra, viene utilizzato l'algoritmo DES per criptare e decriptare il messaggio. Tieni presente che DES è
stato sostituito da algoritmi più sicuri, come ad esempio AES, e non dovrebbe essere utilizzato per la crittografia
di dati sensibili.
"""

import base64
from Cryptodome.Cipher import DES

# Chiave di crittografia (deve essere di 8 caratteri)
key = b'password'


# Criptazione del messaggio
def encrypt(key: bytes, message: str) -> str:
    # Creazione dell'oggetto Cipher
    cipher = DES.new(key, DES.MODE_ECB)

    # Padding del messaggio per garantire che sia di lunghezza multipla di 8
    padding = b' ' * (8 - (len(message) % 8))
    padded_message = message.encode('utf-8') + padding

    # Criptazione del messaggio
    encrypted_message = cipher.encrypt(padded_message)

    # Codifica del messaggio criptato in base64
    return base64.b64encode(encrypted_message).decode('utf-8')


# Decriptazione del messaggio
def decrypt(key: bytes, encrypted_message: str) -> str:
    # Decodifica del messaggio criptato dalla codifica base64
    decoded_message = base64.b64decode(encrypted_message.encode('utf-8'))

    # Creazione dell'oggetto Cipher
    cipher = DES.new(key, DES.MODE_ECB)

    # Decriptazione del messaggio
    decrypted_message = cipher.decrypt(decoded_message)

    # Rimozione del padding aggiunto in fase di criptazione
    return decrypted_message.decode('utf-8').rstrip()


# Criptazione del messaggio
message = "Ciao, come va?"
encrypted_message = encrypt(key, message)

# Decriptazione del messaggio
decrypted_message = decrypt(key, encrypted_message)

print(f'Messaggio originale: {message}')
print(f'Messaggio criptato: {encrypted_message}')
print(f'Messaggio decriptato: {decrypted_message}')
