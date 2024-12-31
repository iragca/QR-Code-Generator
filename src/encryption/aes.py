from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64

#NOTE: This is ChatGPT generated code

# Encrypt function using AES
def encrypt_message(message, key):

    try:
        # Create an AES cipher object with CBC mode
        iv = os.urandom(16)  # Initialization vector (random)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Pad the message to make its length a multiple of block size (16 bytes)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(message.encode()) + padder.finalize()

        # Encrypt the message
        encrypted = encryptor.update(padded_data) + encryptor.finalize()

        # Return both the encrypted message and IV (needed for decryption)
        return base64.b64encode(iv + encrypted).decode()
    except Exception as e:
        return f"Error encrypting message: {e}. Try using strings for both parameters."

def decrypt_message(encrypted_message, key):

    try:
        encrypted_data = base64.b64decode(encrypted_message)
        iv = encrypted_data[:16]  # Extract the IV (first 16 bytes)
        encrypted_message = encrypted_data[16:]  # The rest is the encrypted data

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt the message
        decrypted_padded_data = decryptor.update(encrypted_message) + decryptor.finalize()

        # Unpad the message
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

        return decrypted_data.decode()
    except ValueError as e:
        return f"{e.__class__.__name__}: {e} Possible wrong key used."

def generate_random_encryption_key():
    return os.urandom(32)