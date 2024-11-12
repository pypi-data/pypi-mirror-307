from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
import base64
import os

# Funktion zur Schlüsselerzeugung mit Scrypt
def derive_key(password, salt):
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return key

# Funktion zur sicheren Verschlüsselung
def encrypt(password, plain_text):
    salt = os.urandom(16)
    key = derive_key(password, salt)
    
    # AES Verschlüsselung im CBC-Modus
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Padding des Textes, damit er AES-Blockgröße entspricht
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plain_text.encode()) + padder.finalize()
    
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()
    
    # Kombiniere Salt, IV und Cipher Text
    encrypted_data = base64.b64encode(salt + iv + cipher_text).decode()
    return encrypted_data

# Funktion zum Entschlüsseln
def decrypt(password, encrypted_data):
    encrypted_data = base64.b64decode(encrypted_data)
    
    # Extrahiere Salt, IV und Cipher Text
    salt = encrypted_data[:16]
    iv = encrypted_data[16:32]
    cipher_text = encrypted_data[32:]
    
    key = derive_key(password, salt)
    
    # AES Entschlüsselung im CBC-Modus
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    padded_data = decryptor.update(cipher_text) + decryptor.finalize()
    
    # Entferne Padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    try:
        plain_text = unpadder.update(padded_data) + unpadder.finalize()
        return plain_text.decode()
    except ValueError:
        return "Falsches Passwort oder Daten beschädigt!"
