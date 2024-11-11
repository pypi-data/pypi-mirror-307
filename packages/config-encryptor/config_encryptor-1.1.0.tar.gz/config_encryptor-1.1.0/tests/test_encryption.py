# tests/test_encryption.py

import os
from encryption.encryption import encrypt_config, decrypt_config
from encryption.key_manager import generate_key

def test_encryption():
    # Generate key
    generate_key()

    # Encrypt the config
    encrypt_config(input_file='../config.json', output_file='config_encrypted.json')

    # Decrypt the config
    decrypted_config = decrypt_config(input_file='config_encrypted.json')

    # Assert if the decrypted config is a dictionary (valid JSON)
    assert isinstance(decrypted_config, dict), "Decryption failed, output is not a dictionary."

    print("Encryption and decryption test passed.")

if __name__ == "__main__":
    test_encryption()
