from cryptography.fernet import Fernet
import hashlib
from base64 import urlsafe_b64encode

def encrypter(plaintext, password):
    # Generate hash from password, convert to string
    hash = hashlib.md5(password.encode()).hexdigest()
    # Fernet key must be 32 bytes and urlsafe base 64 encoded
    key = urlsafe_b64encode(hash.encode())
    token = Fernet(key)
    ciphertext = token.encrypt(plaintext.encode())
    return ciphertext.decode()

def decrypter(ciphertext, password):
    # Generate hash from password, convert to string
    hash = hashlib.md5(password.encode()).hexdigest()
    # Fernet key must be 32 bytes and urlsafe base 64 encoded
    key = urlsafe_b64encode(hash.encode())
    token = Fernet(key)
    plaintext = token.decrypt(ciphertext.encode())
    return plaintext.decode()

def main():
    plaintext = input("Enter text: ")
    password = input("Enter password: ")
    print(plaintext)
    ciphertext = encrypter(plaintext, password)
    print(ciphertext)
    decryptedtext = decrypter(ciphertext, password)
    print(decryptedtext)

if __name__ == "__main__":
    main()