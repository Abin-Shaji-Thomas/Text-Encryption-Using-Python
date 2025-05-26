# aes_crypto.py
from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open("keys/secret.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    with open("keys/secret.key", "rb") as key_file:
        return key_file.read()

def aes_encrypt(message):
    key = generate_key()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(message.encode())
    with open("output/encrypted_aes.bin", "wb") as file:
        file.write(encrypted)
    return encrypted

def aes_decrypt():
    key = load_key()
    with open("output/encrypted_aes.bin", "rb") as file:
        encrypted = file.read()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted).decode()
    return decrypted
