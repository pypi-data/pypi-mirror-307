# config_encryptor/encryption.py

import json
from cryptography.fernet import Fernet
from .key_manager import load_key

def encrypt_config(input_file='config.json', output_file='config_encrypted.json'):
    """
    Encrypt the entire content of config.json and save it as config_encrypted.json.
    """
    # Load the encryption key
    key = load_key()
    fernet = Fernet(key)

    # Read the original config file
    with open(input_file, 'r') as json_file:
        config_data = json_file.read()

    # Encrypt the content
    encrypted_data = fernet.encrypt(config_data.encode())

    # Save the encrypted data to a new file
    with open(output_file, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

    print(f"Config file {input_file} has been encrypted and saved as {output_file}.")

def encrypt_json(input_json='config.json', output_file='config_encrypted.json'):
    """
    Encrypt the entire content of config.json and save it as config_encrypted.json.
    """
    # Load the encryption key
    key = load_key()
    fernet = Fernet(key)



    # Encrypt the content
    encrypted_data = fernet.encrypt(input_json.encode())

    # Save the encrypted data to a new file
    with open(output_file, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

    print(f"Config string {input_json} has been encrypted and saved as {output_file}.")
def decrypt_config(input_file='config_encrypted.json'):
    """
    Decrypt the entire content of config_encrypted.json and return it as a dictionary.
    """
    # Load the encryption key
    key = load_key()
    fernet = Fernet(key)

    # Read the encrypted config file
    with open(input_file, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()

    # Decrypt the content
    decrypted_data = fernet.decrypt(encrypted_data).decode()

    # Convert the decrypted JSON data into a dictionary
    config = json.loads(decrypted_data)

    return config
