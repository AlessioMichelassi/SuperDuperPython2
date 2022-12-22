"""

Blowfish è stato sviluppato da Bruce Schneier nel 1993 ed è stato chiamato in questo modo perché il suo algoritmo di
crittografia utilizza una serie di "soffi" (blow) per criptare e decriptare i dati. Schneier ha scelto questo nome
perché il pesce palla (blowfish in inglese) è un animale resistente che può gonfiarsi per difendersi dai predatori.
Allo stesso modo, l'algoritmo Blowfish è stato progettato per essere robusto e resistente agli attacchi informatici.

 Ecco un esempio di come potrebbe essere possibile utilizzare Python e la libreria pycryptodome per criptare e
 decriptare un messaggio utilizzando l'algoritmo di crittografia a chiave simmetrica Blowfish

 Nell'esempio sopra, viene utilizzato l'algoritmo Blowfish per criptare e decriptare il messaggio. Blowfish è un
 algoritmo di crittografia a chiave simmetrica che utilizza una chiave di almeno 8 caratteri per criptare i dati.
 Tieni presente che esistono algoritmi di crittografia più sicuri, come ad esempio AES, e che Blowfish non dovrebbe
 essere utilizzato per la crittografia di dati sensibili. """

import base64
from Cryptodome.Cipher import Blowfish

# Chiave di crittografia (deve essere di almeno 8 caratteri)
key = b'password123'


# Criptazione del messaggio
def encrypt(key: bytes, message: str) -> str:
    # Creazione dell'oggetto Cipher
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)

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
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)

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
